from __future__ import annotations
import sys
from pathlib import Path

from config import load_config
from core.vault import init_vault, add_file, paste_files
from core.describer import describe_and_store
from ui.fzf_ui import pick_files

# This is the main entry point for the Locky CLI.
# It reads arguments from sys.argv and dispatches to the right function.
#
# The commands you need to support:
#
#   locky add <filepath>
#     - Load config and init the vault
#     - Call add_file() with the given path
#     - After adding, call describe_and_store() to auto-generate a description
#     - Print a confirmation message to the user
#
#   locky paste
#     - Load config and init the vault
#     - Call meta.list_files() to get all files in the vault
#     - Call pick_files() to let the user select files interactively via fzf
#     - Call paste_files() with the selected filenames and Path.cwd() as destination
#     - Print a summary of what was pasted
#
#   locky list
#     - Load config and init the vault
#     - Call meta.list_files() and print each filename
#     - Bonus: also print the description for each file (use meta.get_description())
#
#   (no command / unknown command)
#     - Print a short usage/help message showing the available commands
#
# TODO: Define a `main()` function that handles the above logic using if/elif on sys.argv[1]
# TODO: At the bottom, call main() when this file is run directly


