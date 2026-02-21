from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
# Allows us to interact with the operating system (like reading environment variables)
import os

@dataclass(frozen=True)
class Config:
    # Path to the vault directory where files will be stored
    vault_dir: Path
    # Path to the SQLite database file for metadata
    db_path: Path
    # Path to the folder where pasted files are dropped
    paste_dir: Path

def load_config() -> Config:
    # Get the user's home directory
    home = Path.home()
    # Determine the vault directory
    vault_dir = Path(os.environ.get("TEMPVAULT_DIR", home / "vault")).expanduser()
    # The database file lives inside the vault directory
    db_path = vault_dir / "metadata.sqlite3"
    # Files retrieved from the vault are pasted here by default
    paste_dir = Path(os.environ.get("LOCKY_PASTE_DIR", home / "Locky-files")).expanduser()
    return Config(vault_dir=vault_dir, db_path=db_path, paste_dir=paste_dir)