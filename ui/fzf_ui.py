from __future__ import annotations
import shutil
import subprocess
from pathlib import Path

def check_fzf() -> bool:
    # Check if the 'fzf' fuzzy finder tool is installed and available in PATH
    return shutil.which("fzf") is not None

def pick_files(filenames: list[str], db_path: Path, vault_dir: Path) -> list[str]:
    # If fzf is not installed, print an error and return an empty list
    if not check_fzf():
        print("Error: fzf is not installed")
        return []

    # Build the command to launch fzf with multi-select and file preview
    cmd = [
        "fzf",  # fuzzy finder tool
        "--multi",  # allow selecting multiple files
        "--preview", f"python -m core.preview {db_path} {vault_dir} {{}}",  # show file preview using your preview module
        "--preview-window", "right:50%:wrap",  # preview pane on the right, wrap lines
    ]

    # Run the fzf command as a subprocess, sending the filenames as input
    result = subprocess.run(
        cmd,
        input="\n".join(filenames).encode(),  # provide the file list as input (one per line)
        capture_output=True,  # capture the output so we can process it
    )

    # If fzf was cancelled or interrupted, return an empty list
    if result.returncode in (1, 130):
        return []

    # Split the output into lines, strip whitespace, and return the selected filenames
    return [line.strip() for line in result.stdout.decode().split("\n") if line.strip()]
