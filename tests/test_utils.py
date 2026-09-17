import logging
from pathlib import Path

import pytest

from monugstore.utils.files import find_files, rename_file
from monugstore.utils.json_io import check_dict_jsonable, is_jsonable, read_json, write_json
from monugstore.utils.logging import setup_logger
from monugstore.utils.size import format_size, get_file_size


def test_find_files(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.jpg").write_text("b")
    nested = tmp_path / "sub"
    nested.mkdir()
    (nested / "c.txt").write_text("c")

    found = find_files(str(tmp_path), [".txt"], verbose=True)

    assert sorted(Path(p).name for p in found) == ["a.txt", "c.txt"]
    out = capsys.readouterr().out
    assert "a.txt" in out


def test_find_files_silent(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("a")

    found = find_files(str(tmp_path), [".txt"], verbose=False)

    assert len(found) == 1
    assert capsys.readouterr().out == ""


def test_rename_file(tmp_path):
    source = tmp_path / "old.txt"
    source.write_text("hi")

    new_path = rename_file(str(source), "new.txt")

    assert Path(new_path).name == "new.txt"
    assert (tmp_path / "new.txt").read_text() == "hi"
    assert not source.exists()


def test_json_io_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    write_json(str(path), [{"a": 1}])

    assert read_json(str(path)) == [{"a": 1}]


def test_is_jsonable():
    assert is_jsonable({"a": 1}) is True
    assert is_jsonable({1, 2, 3}) is False


def test_check_dict_jsonable_converts_values():
    payload = {"ok": 1, "bad": {1, 2}}

    result = check_dict_jsonable(payload)

    assert result["ok"] == 1
    assert result["bad"] == "{1, 2}"
    assert payload is result


def test_get_file_size(tmp_path):
    path = tmp_path / "f.bin"
    path.write_bytes(b"abcd")

    assert get_file_size(str(path)) == 4


def test_get_file_size_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        get_file_size(str(tmp_path / "missing.bin"))


@pytest.mark.parametrize(
    "size,expected",
    [
        (0, "0.00 B"),
        (1024, "1024.00 B"),
        (1025, "1.00 KB"),
        (1024 ** 2 + 1, "1.00 MB"),
    ],
)
def test_format_size(size, expected):
    assert format_size(size) == expected


def test_setup_logger_invalid_level():
    logger = logging.getLogger("test-logger-invalid")
    logger.handlers.clear()
    with pytest.raises(ValueError, match="Invalid log level"):
        setup_logger("test-logger-invalid", "NOPE")
    assert logger.handlers == []


def test_setup_logger_emits_message(capsys):
    logging.getLogger("test-logger-unique").handlers.clear()
    logger = setup_logger("test-logger-unique", "INFO")
    logger.info("hello-from-test")
    captured = capsys.readouterr()
    text = captured.err + captured.out
    assert "hello-from-test" in text
    assert "test-logger-unique" in text


def test_setup_logger_does_not_add_duplicate_handlers():
    name = "test-logger-once"
    logging.getLogger(name).handlers.clear()

    first = setup_logger(name, "INFO")
    second = setup_logger(name, "DEBUG")

    assert first is second
    assert len(first.handlers) == 1
    assert first.level == logging.DEBUG
