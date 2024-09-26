import json

from google.oauth2 import service_account
from google.cloud import secretmanager


class OauthHandler:
    """
    Class to handle OAuth credentials for Google Cloud services.
    """

    @staticmethod
    def credentials_from_json_string(dict_string: str) -> service_account.Credentials:
        """
        Create a credentials object from a JSON string.

        Args:
            dict_string: The JSON string containing the credentials

        Returns:
            The credentials object
        """
        info_dict: dict[str, str] = json.loads(dict_string)
        info_dict["private_key"] = info_dict["private_key"].replace("\\n", "\n")
        return service_account.Credentials.from_service_account_info(info_dict)

    @staticmethod
    def access_secret(project_id: str, secret_id: str, version_id=1):
        """
        Access a secret from the Secret Manager.

        Args:
            project_id: The project ID
            secret_id: The secret ID
            version_id: The version ID (default is 1)

        Returns:
            The secret value
        """
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
