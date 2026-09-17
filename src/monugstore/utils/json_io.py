import json
from typing import Any


def read_json(path_) -> list[dict]:
    '''
    Return a dict or a list of dicts from a given JSON.
    '''
    with open(path_, encoding="utf8") as j:
        return json.load(j)


def write_json(filename: str, source: list[dict],):
    '''
    Writes a list of dicts to a JSON file.
    Filename = example.json
    Source = list of dictionaries.
    '''
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(source, f, ensure_ascii=False, indent=4)


def is_jsonable(x: Any) -> bool:
    """
    Checks if avariable is json serializable.
    Returns a boolean value

    Args:
        x (Any): Any variable

    Returns:
        bool: A boolean value if the variable is JSON serializable
    """
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def check_dict_jsonable(dict_: dict) -> dict:
    """
    Check if a dict is JSON serializable.
    Loops over the keys and values, and if the values
    are not json serializable it converts to string.

    Args:
        dict_ (dict): A dict to be checked

    Returns:
        dict: A converted dict
    """
    for k, v in dict_.items():
        if not is_jsonable(v):
            dict_[k] = str(v)
    return dict_
