import pytest

import monugstore
from monugstore import GCSManager, OauthHandler


def test_public_exports():
    assert monugstore.__all__ == ["GCSManager", "OauthHandler"]
    assert monugstore.GCSManager is GCSManager
    assert monugstore.OauthHandler is OauthHandler


def test_bucket_manager_is_not_importable():
    with pytest.raises(ImportError):
        from monugstore.buckets import BucketManager  # noqa: F401
