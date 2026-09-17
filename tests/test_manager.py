import json
from unittest.mock import MagicMock

import pytest
from google.cloud.exceptions import NotFound

from monugstore import GCSManager


def test_from_json_file_uses_path(patch_gcs, tmp_path):
    creds = tmp_path / "creds.json"
    creds.write_text("{}")

    manager = GCSManager.from_json_file(str(creds))

    patch_gcs["client_cls"].from_service_account_json.assert_called_once_with(str(creds))
    assert manager.client is patch_gcs["client"]


def test_from_json_file_does_not_treat_arg_as_env_var(patch_gcs, monkeypatch, tmp_path):
    creds = tmp_path / "creds.json"
    creds.write_text("{}")
    monkeypatch.delenv("PATH_TO_CREDENTIALS", raising=False)

    GCSManager.from_json_file(str(creds))

    patch_gcs["client_cls"].from_service_account_json.assert_called_once_with(str(creds))


def test_from_json_file_propagates_errors(patch_gcs):
    patch_gcs["client_cls"].from_service_account_json.side_effect = OSError("missing")

    with pytest.raises(OSError, match="missing"):
        GCSManager.from_json_file("/no/such/file.json")


def test_from_json_string_parses_payload(patch_gcs, fake_sa_json):
    manager = GCSManager.from_json_string(fake_sa_json)

    patch_gcs["credentials"].assert_called_once_with(json.loads(fake_sa_json))
    patch_gcs["client_cls"].assert_any_call(credentials=patch_gcs["credentials"].return_value)
    assert manager.client is patch_gcs["client"]


def test_from_json_string_does_not_look_up_env(patch_gcs, fake_sa_json, monkeypatch):
    monkeypatch.delenv("CREDENTIAL_STRING", raising=False)

    GCSManager.from_json_string(fake_sa_json)

    patch_gcs["credentials"].assert_called_once_with(json.loads(fake_sa_json))


def test_from_json_string_invalid_json(patch_gcs):
    with pytest.raises(json.JSONDecodeError):
        GCSManager.from_json_string("not-json")


def test_from_env_reads_named_variable(patch_gcs, fake_sa_json, monkeypatch):
    monkeypatch.setenv("CREDENTIAL_STRING", fake_sa_json)

    manager = GCSManager.from_env("CREDENTIAL_STRING")

    patch_gcs["credentials"].assert_called_once_with(json.loads(fake_sa_json))
    assert manager.client is patch_gcs["client"]


def test_from_env_missing_variable(monkeypatch):
    monkeypatch.delenv("MISSING_CREDS", raising=False)

    with pytest.raises(ValueError, match="Environment variable MISSING_CREDS not set"):
        GCSManager.from_env("MISSING_CREDS")


def test_str(manager):
    assert str(manager) == "GCSManager(project=test-project)"


def test_create_bucket_rejects_positional_name(manager):
    with pytest.raises(TypeError):
        manager.create_bucket("my-bucket")


def test_create_bucket_defaults_to_private(manager, mock_storage_client):
    mock_storage_client.lookup_bucket.return_value = None
    bucket = MagicMock()
    mock_storage_client.bucket.return_value = bucket
    mock_storage_client.create_bucket.return_value = bucket

    result = manager.create_bucket(bucket_name="my-bucket")

    bucket.make_public.assert_not_called()
    mock_storage_client.create_bucket.assert_called_once_with(bucket)
    assert result is bucket


def test_create_bucket_public_opt_in(manager, mock_storage_client):
    mock_storage_client.lookup_bucket.return_value = None
    bucket = MagicMock()
    mock_storage_client.bucket.return_value = bucket
    mock_storage_client.create_bucket.return_value = bucket

    manager.create_bucket(bucket_name="my-bucket", public=True)

    bucket.make_public.assert_called_once_with(recursive=True, future=True)


def test_create_bucket_returns_existing(manager, mock_storage_client):
    existing = MagicMock()
    mock_storage_client.lookup_bucket.return_value = existing
    mock_storage_client.bucket.return_value = existing

    result = manager.create_bucket(bucket_name="my-bucket", public=True)

    mock_storage_client.create_bucket.assert_not_called()
    existing.make_public.assert_not_called()
    assert result is existing


def test_get_bucket_found(manager, mock_storage_client):
    bucket = MagicMock()
    mock_storage_client.get_bucket.return_value = bucket

    assert manager.get_bucket("my-bucket") is bucket


def test_get_bucket_missing(manager, mock_storage_client):
    mock_storage_client.get_bucket.side_effect = NotFound("missing")

    with pytest.raises(NotFound):
        manager.get_bucket("missing")


def test_upload_file_with_prefix(manager, mock_storage_client, tmp_path):
    bucket = MagicMock()
    bucket.get_blob.return_value = None
    blob = MagicMock()
    blob.public_url = "https://example.com/uploads/file.jpg"
    bucket.blob.return_value = blob
    mock_storage_client.get_bucket.return_value = bucket
    source = tmp_path / "file.jpg"
    source.write_bytes(b"img")

    url = manager.upload_file("my-bucket", str(source), "file.jpg", prefix="uploads")

    bucket.blob.assert_called_once_with("uploads/file.jpg")
    blob.upload_from_filename.assert_called_once_with(str(source))
    blob.make_public.assert_not_called()
    assert url == "https://example.com/uploads/file.jpg"


def test_upload_file_without_prefix(manager, mock_storage_client, tmp_path):
    bucket = MagicMock()
    bucket.get_blob.return_value = None
    blob = MagicMock()
    blob.public_url = "https://example.com/file.jpg"
    bucket.blob.return_value = blob
    mock_storage_client.get_bucket.return_value = bucket
    source = tmp_path / "file.jpg"
    source.write_bytes(b"img")

    manager.upload_file("my-bucket", str(source), "file.jpg")

    bucket.blob.assert_called_once_with("file.jpg")


def test_upload_file_public(manager, mock_storage_client, tmp_path):
    bucket = MagicMock()
    bucket.get_blob.return_value = None
    blob = MagicMock()
    blob.public_url = "https://example.com/file.jpg"
    bucket.blob.return_value = blob
    mock_storage_client.get_bucket.return_value = bucket
    source = tmp_path / "file.jpg"
    source.write_bytes(b"img")

    manager.upload_file("my-bucket", str(source), "file.jpg", public=True)

    blob.make_public.assert_called_once()


def test_upload_file_missing_bucket(manager, mock_storage_client, tmp_path):
    mock_storage_client.get_bucket.side_effect = NotFound("missing")
    source = tmp_path / "file.jpg"
    source.write_bytes(b"img")

    with pytest.raises(NotFound):
        manager.upload_file("missing", str(source), "file.jpg")


def test_upload_file_missing_local_file(manager, mock_storage_client):
    bucket = MagicMock()
    mock_storage_client.get_bucket.return_value = bucket

    with pytest.raises(FileNotFoundError):
        manager.upload_file("my-bucket", "/no/such/file.jpg", "file.jpg")
    bucket.blob.assert_not_called()


def test_upload_file_existing_blob(manager, mock_storage_client, tmp_path):
    bucket = MagicMock()
    existing = MagicMock()
    existing.public_url = "https://example.com/file.jpg"
    bucket.get_blob.return_value = existing
    mock_storage_client.get_bucket.return_value = bucket
    source = tmp_path / "file.jpg"
    source.write_bytes(b"img")

    url = manager.upload_file("my-bucket", str(source), "file.jpg")

    assert url == "https://example.com/file.jpg"
    bucket.blob.assert_not_called()


def test_list_files(manager, mock_storage_client):
    bucket = MagicMock()
    blob_a = MagicMock(name="a.txt")
    blob_a.name = "a.txt"
    blob_b = MagicMock(name="b.txt")
    blob_b.name = "prefix/b.txt"
    bucket.list_blobs.return_value = [blob_a, blob_b]
    mock_storage_client.bucket.return_value = bucket

    assert manager.list_files("my-bucket", prefix="prefix") == ["a.txt", "prefix/b.txt"]
    bucket.list_blobs.assert_called_once_with(prefix="prefix")


def test_download_file(manager, mock_storage_client):
    bucket = MagicMock()
    blob = MagicMock()
    bucket.blob.return_value = blob
    mock_storage_client.bucket.return_value = bucket

    manager.download_file("my-bucket", "file.jpg", "/tmp/out.jpg")

    blob.download_to_filename.assert_called_once_with("/tmp/out.jpg")


def test_delete_file_success(manager, mock_storage_client):
    bucket = MagicMock()
    blob = MagicMock()
    bucket.blob.return_value = blob
    mock_storage_client.bucket.return_value = bucket

    manager.delete_file("my-bucket", "file.jpg")
    blob.delete.assert_called_once()


def test_delete_file_error(manager, mock_storage_client):
    mock_storage_client.bucket.side_effect = NotFound("denied")

    with pytest.raises(NotFound):
        manager.delete_file("my-bucket", "file.jpg")


def test_delete_all_files(manager, mock_storage_client):
    blob = MagicMock()
    bucket = MagicMock()
    bucket.list_blobs.return_value = [blob]
    mock_storage_client.get_bucket.return_value = bucket

    manager.delete_all_files("my-bucket")

    blob.delete.assert_called_once()


def test_delete_all_files_missing_bucket(manager, mock_storage_client):
    mock_storage_client.get_bucket.side_effect = NotFound("missing")

    with pytest.raises(NotFound):
        manager.delete_all_files("missing")


def test_delete_bucket(manager, mock_storage_client):
    bucket = MagicMock()
    mock_storage_client.bucket.return_value = bucket

    manager.delete_bucket("my-bucket")

    bucket.delete.assert_called_once()
