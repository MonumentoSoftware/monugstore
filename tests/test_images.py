import importlib
import sys
from pathlib import Path

import pytest

pytest.importorskip("PIL")

from PIL import Image

from monugstore.utils.images import convert_to_webp, create_thumbnail


def _write_png(path: Path, size=(32, 32)):
    Image.new("RGB", size, color=(255, 0, 0)).save(path)


def test_create_thumbnail(tmp_path):
    source = tmp_path / "photo.png"
    dest = tmp_path / "thumb.png"
    _write_png(source, size=(256, 256))

    result = create_thumbnail(str(source), str(dest), size=(32, 32))

    assert result == str(dest)
    with Image.open(dest) as img:
        assert img.size[0] <= 32
        assert img.size[1] <= 32


def test_create_thumbnail_error():
    assert create_thumbnail("/no/such.png", "/tmp/thumb.png") is None


def test_convert_to_webp_lossless(tmp_path):
    source = tmp_path / "photo.png"
    dest = tmp_path / "photo.png"
    _write_png(source)

    convert_to_webp(str(source), str(dest))

    assert (tmp_path / "photo.webp").exists()


def test_convert_to_webp_quality(tmp_path):
    source = tmp_path / "photo.png"
    dest = tmp_path / "out.jpg"
    _write_png(source)

    convert_to_webp(str(source), str(dest), quality=80)

    assert (tmp_path / "out.webp").exists()


def test_convert_to_webp_error():
    convert_to_webp("/no/such.png", "/tmp/out.webp")


def test_images_extra_required(monkeypatch):
    monkeypatch.setitem(sys.modules, "PIL", None)
    monkeypatch.setitem(sys.modules, "PIL.Image", None)
    sys.modules.pop("monugstore.utils.images", None)

    with pytest.raises(ImportError, match=r"monugstore\[images\]"):
        importlib.import_module("monugstore.utils.images")
