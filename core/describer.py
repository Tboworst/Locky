from __future__ import annotations
from pathlib import Path

from core.metadata import MetaStore
from core.ai_desc import describe_file_baseline

# TODO: Define a function called `describe_and_store` that takes:
#   - meta: MetaStore  (the metadata store)
#   - path: Path       (the full path to the file inside the vault)
#
# It should:
#   1. Call describe_file_baseline(path) to generate a short description string
#   2. Call meta.set_description(path.name, description) to save it
#   3. Return the description string so the caller can display it
#
# Hint: path.name gives you just the filename (e.g. "notes.txt") from a full path
