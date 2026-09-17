import os
import pathlib

from .console import console


def find_files(directory: str, extensions: list[str], verbose: bool = True) -> list[str]:
    """
    Find files with specific extensions in a directory and its subdirectories.

    Args:
        directory (str): The directory to search in
        extensions (list[str]): The list of extensions to search for
        verbose (bool): If True, print each path found

    Returns:
        list[str]: The list of file paths found
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    if verbose:
        for file in files:
            console.print(file)
    return files


def rename_file(file_path: str, new_name: str) -> str:
    """
    Rename a file.

    Args:
        path (str): The path to the file
        new_name (str): The new name for the file

    Returns:
        str: The new path to the renamed file
    """
    path = pathlib.Path(file_path)
    # renaming the file
    new_path = path.with_name(new_name)
    path.rename(new_path)
    return str(new_path)
