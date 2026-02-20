from __future__ import annotations
import shutil
from pathlib import Path

#This file contains utility functions for file management, such as creating directories and prompting the user for yes/no input

def ensure_dir(path:Path)-> None:
    #creates a directory 
    path.mkdir(parents=True,exist_ok=True)


def prompt_yes_no(message:str)-> bool:
    answer = input((f"{message}(y/n):")).strip().lower()
    return answer =="y"

#utilizes the shutil libray to copy a file from src to dst, ensuring that the destination directory exists before copying
def copy_file(src: Path, dst: Path) -> None:
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)