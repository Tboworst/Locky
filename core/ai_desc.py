from __future__ import annotations
from pathlib import Path

def describe_file_baseline(path: Path, max_bytes: int = 16000) -> str:
    ext = path.suffix.lower().lstrip(".") or "unknown"

    try:
        raw = path.read_bytes()[:max_bytes]
        text = raw.decode(errors="ignore")
        for line in text.splitlines():
            s = line.strip()
            if s:
                s = s[:140]
                return f"{ext} file - starts with: {s}"
    except Exception:
        pass

    return f"{ext} file - no previable text"