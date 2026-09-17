from google.cloud import storage  # type: ignore[attr-defined]

from .utils.logging import LOG_LEVELS, setup_logger


class BucketManager:

    def __init__(self, logger_debug: LOG_LEVELS = "DEBUG"):
        self.logger = setup_logger("BucketManager", logger_debug)
        self.client = storage.Client()

    def create_bucket(self, bucket_name: str, location: str = "US") -> storage.Bucket:
        bucket = self.client.create_bucket(bucket_name, location=location)
        self.logger.info(f"Bucket {bucket_name} created")
        return bucket

    def make_public(self, bucket: storage.Bucket, recursive: bool = False):
        bucket.make_public(recursive=recursive, future=True)
        self.logger.info(f"Bucket {bucket.name} is now public")
        return bucket

    def delete_all_files(self, bucket: storage.Bucket):
        blobs: list[storage.Blob] = bucket.list_blobs()
        for blob in blobs:
            blob.delete()
        self.logger.info(f"All files in {bucket.name} were deleted")
        return bucket
