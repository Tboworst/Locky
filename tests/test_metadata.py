from __future__ import annotations
import pytest
from pathlib import Path
from core.metadata import MetaStore


@pytest.fixture
def meta(tmp_path):
    # Create a fresh in-memory-style store in a temp directory for each test
    return MetaStore(tmp_path / "test.sqlite3")


def test_upsert_and_list(meta):
    meta.upsert("notes.txt", 100)
    assert meta.list_files() == ["notes.txt"]


def test_list_is_sorted(meta):
    meta.upsert("zebra.txt", 1)
    meta.upsert("apple.txt", 1)
    assert meta.list_files() == ["apple.txt", "zebra.txt"]


def test_set_and_get_description(meta):
    meta.upsert("notes.txt", 100)
    meta.set_description("notes.txt", "A simple text file")
    assert meta.get_description("notes.txt") == "A simple text file"


def test_get_description_missing_file(meta):
    assert meta.get_description("ghost.txt") is None


def test_upsert_preserves_description(meta):
    # Re-adding a file should not wipe its description
    meta.upsert("notes.txt", 100)
    meta.set_description("notes.txt", "My notes")
    meta.upsert("notes.txt", 200)
    assert meta.get_description("notes.txt") == "My notes"


def test_delete_removes_file(meta):
    meta.upsert("notes.txt", 100)
    meta.delete("notes.txt")
    assert meta.list_files() == []


def test_delete_nonexistent_is_safe(meta):
    # Deleting something that doesn't exist should not raise
    meta.delete("ghost.txt")
