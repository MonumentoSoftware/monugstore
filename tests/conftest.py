import json
from unittest.mock import MagicMock, patch

import pytest

from monugstore.manager import GCSManager

FAKE_SERVICE_ACCOUNT = {
    "type": "service_account",
    "project_id": "test-project",
    "private_key_id": "abc",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE\n-----END PRIVATE KEY-----\n",
    "client_email": "sa@test.iam.gserviceaccount.com",
    "client_id": "1",
    "token_uri": "https://oauth2.googleapis.com/token",
}


@pytest.fixture
def fake_sa_json():
    return json.dumps(FAKE_SERVICE_ACCOUNT)


@pytest.fixture
def mock_storage_client():
    client = MagicMock()
    client.project = "test-project"
    return client


@pytest.fixture
def patch_gcs(mock_storage_client):
    mock_cls = MagicMock(return_value=mock_storage_client)
    mock_cls.from_service_account_json.return_value = mock_storage_client
    with patch("google.cloud.storage.Client", mock_cls), patch(
        "monugstore.manager.service_account.Credentials.from_service_account_info",
        return_value=MagicMock(),
    ) as mock_creds:
        yield {
            "client_cls": mock_cls,
            "client": mock_storage_client,
            "credentials": mock_creds,
        }


@pytest.fixture
def manager(patch_gcs, mock_storage_client):
    return GCSManager(mock_storage_client)
