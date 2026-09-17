import json

import pytest

from monugstore.scripts.dump_json import dump_json, main


def test_dump_json(tmp_path):
    path = tmp_path / "creds.json"
    path.write_text(json.dumps({"type": "service_account"}))

    assert json.loads(dump_json(str(path))) == {"type": "service_account"}


def test_main_prints_json(tmp_path, monkeypatch, capsys):
    path = tmp_path / "creds.json"
    path.write_text(json.dumps({"k": "v"}))
    monkeypatch.setattr("sys.argv", ["mgs-dump-key", str(path)])

    main()

    assert json.loads(capsys.readouterr().out) == {"k": "v"}


def test_main_requires_path(monkeypatch):
    monkeypatch.setattr("sys.argv", ["mgs-dump-key"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
