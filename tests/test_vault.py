from __future__ import annotations
import pytest
from pathlib import Path
from config import Config
from core.metadata import MetaStore
from core.vault import init_vault, add_file, paste_files, remove_files


@pytest.fixture
def cfg(tmp_path):
    vault_dir = tmp_path / "vault"
    paste_dir = tmp_path / "paste"
    return Config(
        vault_dir=vault_dir,
        db_path=vault_dir / "metadata.sqlite3",
        paste_dir=paste_dir,
    )


@pytest.fixture
def meta(cfg):
    return init_vault(cfg)


@pytest.fixture
def sample_file(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("hello from locky")
    return f


def test_add_file_copies_to_vault(cfg, meta, sample_file):
    add_file(cfg, meta, sample_file)
    assert (cfg.vault_dir / "hello.txt").exists()


def test_add_file_registers_in_metadata(cfg, meta, sample_file):
    add_file(cfg, meta, sample_file)
    assert "hello.txt" in meta.list_files()


def test_add_file_not_found_raises(cfg, meta, tmp_path):
    with pytest.raises(FileNotFoundError):
        add_file(cfg, meta, tmp_path / "ghost.txt")


def test_paste_files_copies_to_dest(cfg, meta, sample_file):
    add_file(cfg, meta, sample_file)
    cfg.paste_dir.mkdir(parents=True, exist_ok=True)
    pasted = paste_files(cfg, ["hello.txt"], cfg.paste_dir)
    assert pasted == ["hello.txt"]
    assert (cfg.paste_dir / "hello.txt").exists()


def test_paste_skips_missing_vault_file(cfg, meta):
    cfg.paste_dir.mkdir(parents=True, exist_ok=True)
    pasted = paste_files(cfg, ["ghost.txt"], cfg.paste_dir)
    assert pasted == []


def test_remove_files_deletes_from_vault_and_meta(cfg, meta, sample_file):
    add_file(cfg, meta, sample_file)
    remove_files(cfg, meta, ["hello.txt"])
    assert not (cfg.vault_dir / "hello.txt").exists()
    assert "hello.txt" not in meta.list_files()


def test_remove_nonexistent_file_is_safe(cfg, meta):
    # Should not raise even if the file was never added
    removed = remove_files(cfg, meta, ["ghost.txt"])
    assert removed == ["ghost.txt"]
