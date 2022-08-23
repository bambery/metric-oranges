import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def get_inputs_dir() -> Path:
    root = get_project_root()
    return root.joinpath("inputs")

def get_class_dir() -> Path:
    root = get_project_root()
    return root.joinpath("classes")
