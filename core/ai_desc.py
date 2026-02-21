from __future__ import annotations
from pathlib import Path
import os

# The anthropic package lets us talk to the Claude API.
import anthropic

def describe_file_baseline(path: Path, max_bytes: int = 16000) -> str:
    ext = path.suffix.lower().lstrip(".") or "unknown"

    # Map common extensions to human-friendly type labels
    type_labels = {
        "py": "Python script", "js": "JavaScript file", "ts": "TypeScript file",
        "html": "HTML file", "css": "CSS stylesheet", "json": "JSON file",
        "md": "Markdown document", "txt": "Text file", "csv": "CSV data file",
        "sh": "Shell script", "yaml": "YAML config", "yml": "YAML config",
        "pdf": "PDF document", "png": "PNG image", "jpg": "JPEG image",
        "jpeg": "JPEG image", "zip": "ZIP archive", "sql": "SQL file",
    }
    label = type_labels.get(ext, f"{ext} file")

    try:
        raw = path.read_bytes()[:max_bytes]
        text = raw.decode(errors="ignore")
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        if not lines:
            return f"{label} — no readable text content"

        # Count meaningful lines to give a sense of file size
        line_count = len(text.splitlines())
        size_hint = f"{line_count} lines" if line_count > 1 else "1 line"

        # Use the first non-comment, non-empty line as the content preview
        preview = None
        for line in lines:
            if not line.startswith(("#", "//", "/*", "*", "<!--")):
                preview = line[:120]
                break
        # Fall back to the very first line if everything is comments
        if not preview:
            preview = lines[0][:120]

        return f"{label} ({size_hint}) — {preview}"
    except Exception:
        pass

    return f"{label} — could not read content"

# Function that will describe the files using AI (Claude API)
def describe_file_ai(path: Path, max_bytes: int = 16000) -> str:
    # In a try block so it falls back to baseline if anything fails (e.g., no API key, network error)
    try:
        # Read up to max_bytes from the file and decode to a string
        content = path.read_bytes()[:max_bytes].decode(errors="ignore")
        # Create an Anthropic client (reads API key from environment variable)
        client = anthropic.Anthropic()
        # Call the Claude API to get a short description of the file
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Fast and cheap model, good for this task
            max_tokens=100,  # Only need a short description
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Describe this file in one sentence. Be specific about what it does or contains "
                        f"(e.g. 'A Python script that calculates student grades' or "
                        f"'A CSV file containing sales data with 3 columns'). "
                        f"File name: {path.name}\n\n{content}"
                    )
                }
            ]
        )
        # Extract and return the text from the response
        return message.content[0].text.strip()
    except Exception:
        # If anything goes wrong, fall back to the baseline description
        return describe_file_baseline(path, max_bytes)
