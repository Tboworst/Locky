from __future__ import annotations
import shutil
import subprocess
from pathlib import Path

# TODO: Define a function called `check_fzf` that:
#   - Returns True if fzf is installed on the system, False otherwise
#   - Hint: use shutil.which("fzf")


# TODO: Define a function called `pick_files` that takes:
#   - filenames: list[str]   (the list of files currently in the vault)
#   - db_path: Path          (path to the metadata database, passed to preview.py)
#   - vault_dir: Path        (path to the vault directory, passed to preview.py)
#
# It should:
#   1. Check that fzf is available — if not, print an error and return an empty list
#   2. Build the fzf command with these flags:
#        --multi              so the user can select multiple files with Tab
#        --preview            to show a live preview pane for the highlighted file
#                             The preview command should call:
#                             python -m core.preview <db_path> <vault_dir> {}
#                             ({} is the fzf placeholder for the currently highlighted item)
#        --preview-window     your choice of layout (e.g. "right:50%:wrap")
#   3. Run the fzf command via subprocess, passing the filenames list as stdin
#      (join filenames with newlines "\n" and encode to bytes)
#   4. Capture stdout and return the selected filenames as a list of strings
#      (split stdout by newlines, strip whitespace, filter out empty strings)
#   5. If the user cancels fzf (return code 130 or 1), return an empty list
