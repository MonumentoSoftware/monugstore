from abc import ABC, abstractmethod
import json
from typing import List
import os
import pathlib

from google.oauth2 import service_account
from google.cloud import storage
from dotenv import load_dotenv

from monugstore.buckets import BucketManager

from .utils.logging import setup_logger


class GCSManagerInterface(ABC):
    @abstractmethod
    def create_bucket(self, bucket_name: str, location: str = "US") -> storage.Bucket:
        pass

    @abstractmethod
    def get_bucket(self, bucket_name: str) -> storage.Bucket:
        pass

    @abstractmethod
    def upload_file(self, bucket_name: str, file_path: str, destination_blob_name: str) -> str:
        pass

    @abstractmethod
    def list_files(self, bucket_name: str, prefix: str = "") -> List[str]:
        pass

    @abstractmethod
    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
        pass

    @abstractmethod
    def delete_file(self, bucket_name: str, blob_name: str) -> None:
        pass

    @abstractmethod
    def delete_bucket(self, bucket_name: str) -> None:
        pass

# A decorator that looks if the bucket already exists
# It checks if the bucket exists and if it does, it logs a message and returns the bucket object
# If the bucket does not exist, return None. This is a good way to handle the case where the bucket already exists.


class BucketExistsDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(args)
        print(kwargs)


class GCSManager:
    """
    Class to manage Google Cloud Storage (GCS) operations.
    It requires a Google Cloud Storage client object.
    There are two class methods to create a GCSManager object:
    - from_credentials: Create a GCSManager object from a service account credentials object
    - from_json_file: Create a GCSManager object from a service account JSON file
    """

    logger = setup_logger("GCSManager")

    def __init__(self, client: storage.Client) -> None:
        self.client = client
        self.buckets = BucketManager()

    def __load_env(self, env_variable: str) -> str:
        """
        Load the enviromental variable containing the service account JSON string and
        create a service account credentials object.

        Args:
            env_variable (str): The name of the enviromental variable

        Returns:
            service_account.Credentials: The service account credentials object
        """
        load_dotenv()
        if not os.getenv(env_variable):
            raise Exception(f"Environment variable {env_variable} not set.")
        return os.getenv(env_variable)

    @classmethod
    def from_json_string(cls, env_variable: str) -> "GCSManager":
        """
        Create a GCSManager object from a enviromental variable containing a service account JSON string.
        Loads the enviromental variable and creates a service account credentials object.
        Passes the credentials object to the storage client object.

        Args:
            env_variable (str): The name of the enviromental variable containing the service account JSON string

        Returns:
            GCSManager: The GCSManager object
        """
        cls.logger.debug(f"Creating GCSManager from JSON string in environment variable {env_variable}.")
        try:
            if not os.getenv(env_variable):
                raise Exception(f"Environment variable {env_variable} not set.")

            cred = service_account.Credentials.from_service_account_info(json.loads(os.getenv(env_variable)))
            client = storage.Client(credentials=cred)
            return cls(client)
        except Exception as e:
            cls.logger.error(f"Error creating GCSManager: {e}")
            raise Exception(f"Error creating GCSManager: {e}")

    @classmethod
    def from_json_file_path(cls, json_file_path: str) -> "GCSManager":
        """
        Create a GCSManager object from a service account JSON file.

        Args:
            json_file_path (str): The path to the JSON file

        Returns:
            GCSManager: The GCSManager object
        """
        load_dotenv()
        path = cls.__load_env(cls, json_file_path)
        try:
            client = storage.Client.from_service_account_json(path)
            return cls(client)
        except Exception as e:
            raise Exception(f"Error creating GCSManager: {e}")

    def __str__(self) -> str:
        return f"GCSManager(project={self.client.project})"

    def create_bucket(self, *, bucket_name: str, location: str = "US", public: bool = True) -> storage.Bucket:
        """
        Create a new bucket in the specified location.

        :param bucket_name: The name of the bucket to create
        :param location: The location for the bucket (default is "US")
        :return: The created bucket object
        """
        # Check if the bucket already exists
        if self.client.lookup_bucket(bucket_name):
            self.logger.info(f"Bucket {bucket_name} already exists.")
            return self.client.bucket(bucket_name)

        bucket = self.client.bucket(bucket_name)
        bucket.location = location
        bucket = self.client.create_bucket(bucket)
        if public:
            bucket.make_public(recursive=True, future=True)
        self.logger.info(f"Bucket {bucket_name} created in {location}.")
        return bucket

    def get_bucket(self, bucket_name: str) -> storage.Bucket:
        """
        Get a bucket by name.

        Args:
            bucket_name (str): The name of the bucket

        Returns:
            storage.Bucket: The bucket object
        """
        if not self.client.lookup_bucket(bucket_name):
            self.logger.error(f"Bucket {bucket_name} not found.")
            return None
        bucket = self.client.bucket(bucket_name)
        return bucket

    def upload_file(self, bucket_name: str, file_path: str, destination_blob_name: str, prefix: str, public=False) -> str:  # noqa
        """
        Upload a file to the specified bucket.

        Args:
            bucket_name (str): The name of the bucket
            file_path (str): The local path to the file
            destination_blob_name (str): The name of the blob in the bucket

        Returns:
            str: The public URL of the uploaded file
        """
        bucket = self.get_bucket(bucket_name)
        destination_path = f"{prefix}/{destination_blob_name}"
        # Check if the file is file
        if not pathlib.Path(file_path).is_file():
            self.logger.error(f"File {file_path} not found.")
            return None
        if bucket.get_blob(destination_path):
            self.logger.info(f"Blob {destination_path} already exists in bucket {bucket_name}.")
            return None
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(file_path)
        if public:
            blob.make_public()
        self.logger.info(f"File {file_path} uploaded to {destination_path}.")
        return blob.public_url

    def list_files(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        List all files in a specified bucket with an optional prefix.

        Args:
            bucket_name (str): The name of the bucket
            prefix (str): The prefix to filter the files (default is "")

        Returns:
            List[str]: The list of file names
        """
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        file_list = [blob.name for blob in blobs]
        return file_list

    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
        """
        Download a file from a bucket to a local file.

        Args:
            bucket_name (str): The name of the bucket
            source_blob_name (str): The name of the blob to download
            destination_file_name (str): The local file path to save the downloaded

        Returns:
            None
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        self.logger.info(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

    def delete_file(self, bucket_name: str, blob_name: str) -> None:
        """
        Delete a file from a bucket.

        Args:
            bucket_name (str): The name of the bucket
            blob_name (str): The name of the blob to delete

        Returns:
            None
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            self.logger.info(f"Blob {blob_name} deleted from bucket {bucket_name}.")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting blob {blob_name} from bucket {bucket_name}: {e}")
            return False

    def delete_bucket(self, bucket_name: str) -> None:
        """
        Delete a bucket. The bucket must be empty before it can be deleted.

        Args:
            bucket_name (str): The name of the bucket to delete

        Returns:
            None
        """
        bucket = self.client.bucket(bucket_name)
        bucket.delete()
        self.logger.info(f"Bucket {bucket_name} deleted.")
