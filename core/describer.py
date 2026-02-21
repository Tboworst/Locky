from __future__ import annotations
from pathlib import Path
import os

from core.metadata import MetaStore
from core.ai_desc import describe_file_ai, describe_file_baseline

def describe_and_store(meta: MetaStore, path: Path) -> str:
    # Check if the ANTHROPIC_API_KEY environment variable is set
    if os.environ.get("ANTHROPIC_API_KEY"):
        # If the API key exists, use the AI-powered description
        description = describe_file_ai(path)
    else:
        # If the API key doesn't exist, use the baseline (non-AI) description
        description = describe_file_baseline(path)   

    # Store the description in the metadata database
    meta.set_description(path.name, description)
    # Return the description
    return description
