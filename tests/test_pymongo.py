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
