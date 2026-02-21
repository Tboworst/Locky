from __future__ import annotations
from pathlib import Path
import os

# The anthropic package lets us talk to the Claude API.
import anthropic

def describe_file_baseline(path: Path, max_bytes: int = 16000) -> str:
    # Get the file extension (without the dot), or "unknown" if none
    ext = path.suffix.lower().lstrip(".") or "unknown"

    try:
        # Read up to max_bytes from the file as raw bytes
        raw = path.read_bytes()[:max_bytes]
        # Decode the bytes to text, ignoring any decode errors
        text = raw.decode(errors="ignore")
        # Go through each line in the decoded text
        for line in text.splitlines():
            s = line.strip()  # Remove leading/trailing whitespace
            if s:
                s = s[:140]  # Limit the preview to 140 characters
                # Return a description with the file type and the first non-empty line
                return f"{ext} file - starts with: {s}"
    except Exception:
        # If anything goes wrong (e.g., file can't be read), ignore the error
        pass

    # Fallback: if no previewable text was found or an error occurred
    return f"{ext} file - no previable text"

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
                    "content": f"Describe this file in one short sentence:\n\n{content}"
                }
            ]
        )
        # Extract and return the text from the response
        return message.content[0].text.strip()
    except Exception:
        # If anything goes wrong, fall back to the baseline description
        return describe_file_baseline(path, max_bytes)
