import importlib
import sys
from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("pymongo")

from monugstore.pymongo import get_client


@patch("monugstore.pymongo.MongoClient")
def test_get_client_success(mock_cls):
    client = MagicMock()
    mock_cls.return_value = client

    assert get_client("mongodb://localhost") is client
    mock_cls.assert_called_once_with("mongodb://localhost")


@patch("monugstore.pymongo.MongoClient", side_effect=RuntimeError("boom"))
def test_get_client_error(mock_cls, capsys):
    assert get_client("mongodb://localhost") is None
    assert "Error: boom" in capsys.readouterr().out


def test_mongo_extra_required(monkeypatch):
    monkeypatch.setitem(sys.modules, "pymongo", None)
    sys.modules.pop("monugstore.pymongo", None)

    with pytest.raises(ImportError, match=r"monugstore\[mongo\]"):
        importlib.import_module("monugstore.pymongo")
