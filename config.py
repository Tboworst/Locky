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

def load_config() -> Config:
    # Get the user's home directory
    home = Path.home()
    # Determine the vault directory:
    # If the TEMPVAULT_DIR environment variable is set, use its value.
    # Otherwise, default to a "tempvault" directory in the user's home.
    vault_dir = Path(os.environ.get("TEMPVAULT_DIR", home / "vault")).expanduser()
    # The database file will be named "metadata.sqlite3" inside the vault directory
    db_path = vault_dir / "metadata.sqlite3"
    # Return a Config object with the determined paths
    return Config(vault_dir=vault_dir, db_path=db_path)