# Locky

A file vault for your terminal. Add anything, find it instantly, paste it anywhere.

Powered by Claude AI — every file you store gets an automatic description so you always know what's inside without opening it.

> **Work in progress** — core features are working but more is coming (see roadmap below).

---

## What it does

Locky lets you stash files in a central vault and retrieve them fast. When you add a file, Claude AI automatically writes a description so you always know what's inside without opening it.

---

## Demo

<!-- Add your video here -->

---

## Requirements

- Python 3.10+
- [fzf](https://github.com/junegunn/fzf) (`brew install fzf`)
- An Anthropic API key (optional — falls back to a plain description without it)

---

## Installation

```bash
git clone https://github.com/Tboworst/Locky.git
cd Locky
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

To enable AI descriptions, add your key to your shell:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

---

## Commands

| Command | What it does |
|---|---|
| `locky add` | Open a file browser and pick a file to add to the vault |
| `locky add <filepath>` | Add a specific file directly |
| `locky list` | List all files in the vault with their descriptions |
| `locky paste` | Browse the vault and paste selected files into `~/Locky-files` |
| `locky remove` | Browse the vault and permanently delete selected files |

---

## Example workflow

```bash
# Store a file
locky add

# See what's in the vault
locky list

# Go to a project folder and pull a file from the vault
cd ~/my-project
locky paste
```

---

## Roadmap

- [x] `locky remove` — delete a file from the vault
- [ ] `locky search` — search descriptions with natural language via Claude
- [ ] Auto-refresh descriptions on re-add
- [ ] README demo video

---

## Built with

- [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) — AI file descriptions via Claude Haiku
- [fzf](https://github.com/junegunn/fzf) — fuzzy file browser
- SQLite — lightweight metadata storage

---

*Built with assistance from [Claude](https://claude.ai) (Anthropic).*
