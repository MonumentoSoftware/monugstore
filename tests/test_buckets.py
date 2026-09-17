from unittest.mock import MagicMock, patch

from monugstore.buckets import BucketManager


@patch("monugstore.buckets.storage.Client")
def test_create_bucket(mock_client_cls):
    client = mock_client_cls.return_value
    bucket = MagicMock()
    client.create_bucket.return_value = bucket

    manager = BucketManager()
    result = manager.create_bucket("my-bucket", location="EU")

    client.create_bucket.assert_called_once_with("my-bucket", location="EU")
    assert result is bucket


@patch("monugstore.buckets.storage.Client")
def test_make_public(mock_client_cls):
    bucket = MagicMock()
    bucket.name = "my-bucket"
    manager = BucketManager()

    result = manager.make_public(bucket, recursive=True)

    bucket.make_public.assert_called_once_with(recursive=True, future=True)
    assert result is bucket


@patch("monugstore.buckets.storage.Client")
def test_delete_all_files_success(mock_client_cls):
    blob = MagicMock()
    bucket = MagicMock()
    bucket.name = "my-bucket"
    bucket.list_blobs.return_value = [blob]
    manager = BucketManager()

    result = manager.delete_all_files(bucket)

    blob.delete.assert_called_once()
    assert result is bucket


@patch("monugstore.buckets.storage.Client")
def test_delete_all_files_error(mock_client_cls):
    bucket = MagicMock()
    bucket.name = "my-bucket"
    bucket.list_blobs.side_effect = RuntimeError("denied")
    manager = BucketManager()

    assert manager.delete_all_files(bucket) is None
