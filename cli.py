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
def main():
    cfg = load_config()
    meta = init_vault(cfg)

    if len(sys.argv) < 2:
        print("Locky — file vault")
        print("")
        print("Commands:")
        print("  locky add <filepath>   Add a file to the vault")
        print("  locky paste            Pick files from the vault and paste them here")
        print("  locky list             List all files in the vault")
        return

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: locky add <filepath>")
            return
        path = Path(sys.argv[2])
        try:
            add_file(cfg, meta, path)
        except FileNotFoundError:
            print(f"Error: file not found: {path}")
            return
        desc = describe_and_store(meta, cfg.vault_dir / path.name)
        print(f"Added '{path.name}'")
        print(f"Description: {desc}")

    elif cmd == "paste":
        files = meta.list_files()
        if not files:
            print("Vault is empty.")
            return
        selected = pick_files(files, cfg.db_path, cfg.vault_dir)
        if not selected:
            print("Nothing selected.")
            return
        pasted = paste_files(cfg, selected, Path.cwd())
        print(f"Pasted {len(pasted)} file(s): {', '.join(pasted)}")

    elif cmd == "list":
        files = meta.list_files()
        if not files:
            print("Vault is empty.")
            return
        for name in files:
            desc = meta.get_description(name) or "no description"
            print(f"  {name}  —  {desc}")

    else:
        print(f"Unknown command: '{cmd}'")
        print("Run 'locky' with no arguments for help.")


if __name__ == "__main__":
    main()
