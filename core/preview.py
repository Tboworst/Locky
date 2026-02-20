from __future__ import annotations
import sys
import sqlite3
import shutil
import subprocess
from pathlib import Path

def get_description(db_path: Path, filename: str) -> str | None:
    # Check if the database file exists
    if not db_path.exists():
        return None
    # Connect to the SQLite database
    con = sqlite3.connect(db_path)
    try:
        # Query for the description of the given filename
        row = con.execute("SELECT description FROM files WHERE filename=?", (filename,)).fetchone()
        # Return the description if found and not empty, else None
        return row[0] if row and row[0] else None
    finally:
        # Always close the database connection
        con.close()

def pick_preview_cmd():
    # Check if the 'bat' CLI tool is installed (for pretty file previews)
    if shutil.which("bat"):
        # Use 'bat' with line numbers and colored output
        return ["bat", "--style=numbers", "--color=always"]
    # Check for 'batcat' (sometimes installed as 'batcat' on some systems)
    if shutil.which("batcat"):
        return ["batcat", "--style=numbers", "--color=always"]
    # Fallback to 'cat' if neither is available (plain output)
    return ["cat"]

def main(argv: list[str]) -> int:
    # Ensure the correct number of arguments are provided
    if len(argv) != 4:
        return 1  # Return error code if arguments are missing

    # Parse command-line arguments
    db_path = Path(argv[1])      # Path to the metadata database
    vault_dir = Path(argv[2])    # Path to the vault directory
    filename = argv[3]           # Name of the file to preview

    file_path = vault_dir / filename  # Full path to the file in the vault
    desc = get_description(db_path, filename)  # Get file description from database

    # Print file info and description
    print(f"File: {filename}")
    print(f"Description: {desc if desc else '(none)'}")
    print("-" * 60)  # Separator line

    # Check if the file exists and is a regular file
    if not file_path.exists() or not file_path.is_file():
        print("(file not found in vault)")
        return 0  # Exit gracefully if file is missing

    # Build the preview command and run it to display the file contents
    cmd = pick_preview_cmd() + [str(file_path)]
    subprocess.run(cmd, check=False)
    return 0  # Success

if __name__ == "__main__":
    # Run the main function with command-line arguments and exit with its status code
    raise SystemExit(main(sys.argv))