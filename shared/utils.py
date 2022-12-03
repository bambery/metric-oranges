import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def get_inputs_dir() -> Path:
    root = get_project_root()
    return root.joinpath("inputs")

def get_outputs_dir() -> Path:
    root = get_project_root()
    return root.joinpath("outputs")

def get_class_dir() -> Path:
    root = get_project_root()
    return root.joinpath("classes")

def set_pd_display():
    pd.set_option('display.width', 200)
    pd.set_option('display.max_columns', None)

def sort_dict_by_val_desc(dic):
    return dict(sorted(dic.items(), key=lambda x:x[1], reverse=True))
