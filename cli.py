from __future__ import annotations
import sys
from pathlib import Path

# Import configuration loader and core functionality
from config import load_config
from core.vault import init_vault, add_file, paste_files
from core.describer import describe_and_store
from ui.fzf_ui import pick_files, pick_file_to_add

def main():
    # Load configuration (vault directory, database path)
    cfg = load_config()
    # Initialize the vault and metadata store
    meta = init_vault(cfg)

    # If no command is provided, print help and exit
    if len(sys.argv) < 2:
        print("Locky — file vault")
        print("")
        print("Commands:")
        print("  locky add              Browse and pick a file to add to the vault")
        print("  locky add <filepath>   Add a specific file to the vault")
        print("  locky paste            Pick files from the vault and paste them here")
        print("  locky list             List all files in the vault")
        return

    # Get the command from the command-line arguments
    cmd = sys.argv[1]

    if cmd == "add":
        # If no file given, open fzf to browse and pick one
        if len(sys.argv) < 3:
            path = pick_file_to_add(Path.home())
            if path is None:
                return
        else:
            path = Path(sys.argv[2])
        try:
            # Add the file to the vault and metadata database
            add_file(cfg, meta, path)
        except FileNotFoundError:
            print(f"Error: file not found: {path}")
            return
        # Generate and store a description for the file
        desc = describe_and_store(meta, cfg.vault_dir / path.name)
        print(f"Added '{path.name}'")
        print(f"Description: {desc}")

    elif cmd == "paste":
        # Paste files from the vault to the current working directory
        files = meta.list_files()
        if not files:
            print("Vault is empty.")
            return
        # Let the user pick files interactively using fzf
        selected = pick_files(files, cfg.db_path, cfg.vault_dir)
        if not selected:
            print("Nothing selected.")
            return
        # Copy the selected files to the current directory
        pasted = paste_files(cfg, selected, Path.cwd())
        print(f"Pasted {len(pasted)} file(s): {', '.join(pasted)}")

    elif cmd == "list":
        # List all files in the vault with their descriptions
        files = meta.list_files()
        if not files:
            print("Vault is empty.")
            return
        for name in files:
            desc = meta.get_description(name) or "no description"
            print(f"  {name}  —  {desc}")

    else:
        # Handle unknown commands
        print(f"Unknown command: '{cmd}'")
        print("Run 'locky' with no arguments for help.")

if __name__ == "__main__":
    # Run the main function if this script is executed directly
    main()
