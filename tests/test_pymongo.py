import importlib
import logging
import sys
from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("pymongo")

from pymongo.errors import PyMongoError

from monugstore.pymongo import get_client


@patch("monugstore.pymongo.MongoClient")
def test_get_client_success(mock_cls):
    client = MagicMock()
    mock_cls.return_value = client

    assert get_client("mongodb://localhost") is client
    mock_cls.assert_called_once_with("mongodb://localhost")


@patch("monugstore.pymongo.MongoClient", side_effect=PyMongoError("boom"))
def test_get_client_error(mock_cls, caplog):
    with caplog.at_level(logging.ERROR):
        assert get_client("mongodb://localhost") is None
    assert "mongo_client_failed" in caplog.text
    assert "mongodb://localhost" not in caplog.text


def test_mongo_extra_required(monkeypatch):
    monkeypatch.setitem(sys.modules, "pymongo", None)
    sys.modules.pop("monugstore.pymongo", None)

    with pytest.raises(ImportError, match=r"monugstore\[mongo\]"):
        importlib.import_module("monugstore.pymongo")
