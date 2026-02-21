from __future__ import annotations
import sys
from pathlib import Path

from config import load_config
from core.vault import init_vault, add_file, paste_files, remove_files
from core.describer import describe_and_store
from ui.fzf_ui import pick_files, pick_file_to_add


def main():
    cfg = load_config()
    meta = init_vault(cfg)

    if len(sys.argv) < 2:
        print("Locky — file vault")
        print("")
        print("Commands:")
        print("  locky add              Browse and pick a file to add to the vault")
        print("  locky add <filepath>   Add a specific file to the vault")
        print("  locky paste            Pick files from the vault and paste them to ~/Locky-files")
        print("  locky list             List all files in the vault with descriptions")
        print("  locky remove           Browse the vault and remove selected files")
        return

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) < 3:
            path = pick_file_to_add(Path.home())
            if path is None:
                return
        else:
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
        # Ensure the paste folder exists
        cfg.paste_dir.mkdir(parents=True, exist_ok=True)
        pasted = paste_files(cfg, selected, cfg.paste_dir)
        if pasted:
            print(f"\nPasted {len(pasted)} file(s) to {cfg.paste_dir}:")
            for name in pasted:
                print(f"  {name}")

    elif cmd == "list":
        files = meta.list_files()
        if not files:
            print("Vault is empty.")
            return
        for name in files:
            desc = meta.get_description(name) or "no description"
            print(f"  {name}  —  {desc}")

    elif cmd == "remove":
        files = meta.list_files()
        if not files:
            print("Vault is empty.")
            return
        selected = pick_files(files, cfg.db_path, cfg.vault_dir)
        if not selected:
            print("Nothing selected.")
            return
        removed = remove_files(cfg, meta, selected)
        print(f"\nRemoved {len(removed)} file(s) from vault:")
        for name in removed:
            print(f"  {name}")

    else:
        print(f"Unknown command: '{cmd}'")
        print("Run 'locky' with no arguments for help.")


if __name__ == "__main__":
    main()
