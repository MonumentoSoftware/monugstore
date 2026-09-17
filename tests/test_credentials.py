from unittest.mock import MagicMock, patch

from monugstore.credentials import ServiceAccountCredentials


def test_credentials_from_json_string_unescapes_private_key():
    # After json.loads, private_key still contains literal \n sequences.
    raw = '{"private_key": "-----BEGIN PRIVATE KEY-----\\\\nLINE\\\\n-----END PRIVATE KEY-----\\\\n"}'

    with patch(
        "monugstore.credentials.service_account.Credentials.from_service_account_info",
        return_value=MagicMock(),
    ) as mock_creds:
        ServiceAccountCredentials.credentials_from_json_string(raw, escape=True)
        info = mock_creds.call_args[0][0]
        assert info["private_key"] == ("-----BEGIN PRIVATE KEY-----\nLINE\n-----END PRIVATE KEY-----\n")


def test_credentials_from_json_string_without_escape():
    raw = '{"private_key": "-----BEGIN PRIVATE KEY-----\\\\nLINE\\\\n-----END PRIVATE KEY-----\\\\n"}'

    with patch(
        "monugstore.credentials.service_account.Credentials.from_service_account_info",
        return_value=MagicMock(),
    ) as mock_creds:
        ServiceAccountCredentials.credentials_from_json_string(raw, escape=False)
        info = mock_creds.call_args[0][0]
        assert info["private_key"] == ("-----BEGIN PRIVATE KEY-----\\nLINE\\n-----END PRIVATE KEY-----\\n")


def test_access_secret():
    client = MagicMock()
    client.access_secret_version.return_value.payload.data = b"secret-value"

    with patch("monugstore.credentials.secretmanager.SecretManagerServiceClient", return_value=client):
        value = ServiceAccountCredentials.access_secret("proj", "my-secret", version_id=2)

    client.access_secret_version.assert_called_once_with(request={"name": "projects/proj/secrets/my-secret/versions/2"})
    assert value == "secret-value"
