import json
from typing import List
import os

from google.oauth2 import service_account
from google.cloud import storage
from dotenv import load_dotenv

from .utils.logging import setup_logger


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

    @classmethod
    def from_json_string(cls, env_variable: str) -> "GCSManager":
        """
        Create a GCSManager object from a service account credentials object.

        Args:
            credentials (service_account.Credentials): The credentials object

        Returns:
            GCSManager: The GCSManager object
        """
        try:
            # check if the environment variable is set
            if not os.getenv(env_variable):
                load_dotenv()
            cred = service_account.Credentials.from_service_account_info(json.loads(os.getenv(env_variable)))
            client = storage.Client(credentials=cred)
            return cls(client)
        except Exception as e:
            cls.logger.error(f"Error creating GCSManager: {e}")
            raise Exception(f"Error creating GCSManager: {e}")

    @classmethod
    def from_json_file(cls, json_file_path: str) -> "GCSManager":
        """
        Create a GCSManager object from a service account JSON file.

        Args:
            json_file_path (str): The path to the JSON file

        Returns:
            GCSManager: The GCSManager object
        """
        try:
            client = storage.Client.from_service_account_json(json_file_path)
            return cls(client)
        except Exception as e:
            raise Exception(f"Error creating GCSManager: {e}")

    def __str__(self) -> str:
        return f"GCSManager(project={self.client.project})"

    def create_bucket(self, bucket_name: str, location: str = "US") -> storage.Bucket:
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
        self.logger.info(f"Bucket {bucket_name} created in {location}.")
        self.logger.info(f"Bucket {bucket_name} created in {location}.")
        return bucket

    def upload_file(self, bucket_name: str, file_path: str, destination_blob_name: str) -> str:
        """
        Upload a file to the specified bucket.

        Args:
            bucket_name (str): The name of the bucket
            file_path (str): The local path to the file
            destination_blob_name (str): The name of the blob in the bucket

        Returns:
            str: The public URL of the uploaded file
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        self.logger.info(f"File {file_path} uploaded to {destination_blob_name}.")
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
