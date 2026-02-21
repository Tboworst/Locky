from __future__ import annotations
import pytest
from pathlib import Path
from core.ai_desc import describe_file_baseline


@pytest.fixture
def tmp_file(tmp_path):
    def _make(name: str, content: str):
        f = tmp_path / name
        f.write_text(content)
        return f
    return _make


def test_python_file_label(tmp_file):
    f = tmp_file("script.py", "# comment\ndef main():\n    pass\n")
    desc = describe_file_baseline(f)
    assert desc.startswith("Python script")


def test_text_file_label(tmp_file):
    f = tmp_file("notes.txt", "Hello world")
    desc = describe_file_baseline(f)
    assert desc.startswith("Text file")


def test_line_count_included(tmp_file):
    f = tmp_file("data.txt", "line1\nline2\nline3\n")
    desc = describe_file_baseline(f)
    assert "3 lines" in desc


def test_skips_comment_lines(tmp_file):
    # First real line after comments should appear in description
    f = tmp_file("script.py", "# author: tbo\ndef greet():\n    pass\n")
    desc = describe_file_baseline(f)
    assert "def greet" in desc


def test_empty_file_fallback(tmp_file):
    f = tmp_file("empty.txt", "")
    desc = describe_file_baseline(f)
    assert "no readable text" in desc


def test_unknown_extension(tmp_file):
    f = tmp_file("myfile.xyz", "some content here")
    desc = describe_file_baseline(f)
    assert "xyz file" in desc
