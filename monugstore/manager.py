from google.cloud import storage
from typing import List, Optional


class GCSManager:
    def __init__(self, project_name: str, credentials_json: Optional[str] = None):
        """
        Initialize the GCSManager with the specified project and optional credentials.

        :param project_name: Google Cloud project name
        :param credentials_json: Path to the service account JSON file (optional)
        """
        if credentials_json:
            self.client = storage.Client.from_service_account_json(credentials_json)
        else:
            self.client = storage.Client(project=project_name)

    def create_bucket(self, bucket_name: str, location: str = "US") -> storage.Bucket:
        """
        Create a new bucket in the specified location.

        :param bucket_name: The name of the bucket to create
        :param location: The location for the bucket (default is "US")
        :return: The created bucket object
        """
        bucket = self.client.bucket(bucket_name)
        bucket.location = location
        bucket = self.client.create_bucket(bucket)
        print(f"Bucket {bucket_name} created.")
        return bucket

    def upload_file(self, bucket_name: str, file_path: str, destination_blob_name: str) -> str:
        """
        Upload a file to the specified bucket.

        :param bucket_name: The name of the bucket
        :param file_path: The path of the file to upload
        :param destination_blob_name: The destination path/name in the bucket
        :return: The public URL of the uploaded file
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to {destination_blob_name}.")
        return blob.public_url

    def list_files(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        List all files in a specified bucket with an optional prefix.

        :param bucket_name: The name of the bucket
        :param prefix: Prefix to filter files (e.g., "app1/user1/")
        :return: List of file paths
        """
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        file_list = [blob.name for blob in blobs]
        return file_list

    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
        """
        Download a file from a bucket to a local file.

        :param bucket_name: The name of the bucket
        :param source_blob_name: The name of the blob in the bucket
        :param destination_file_name: The local path to save the file
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

    def delete_file(self, bucket_name: str, blob_name: str) -> None:
        """
        Delete a file from a bucket.

        :param bucket_name: The name of the bucket
        :param blob_name: The name of the blob to delete
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print(f"Blob {blob_name} deleted from bucket {bucket_name}.")

    def delete_bucket(self, bucket_name: str) -> None:
        """
        Delete a bucket. The bucket must be empty before it can be deleted.

        :param bucket_name: The name of the bucket to delete
        """
        bucket = self.client.bucket(bucket_name)
        bucket.delete()
        print(f"Bucket {bucket_name} deleted.")
