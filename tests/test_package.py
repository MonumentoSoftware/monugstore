from monugstore import GCSManager, OauthHandler
from monugstore.utils.console import console


def test_public_exports():
    assert GCSManager is not None
    assert OauthHandler is not None
    assert console is not None
