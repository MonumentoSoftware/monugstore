import os


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path (str): The path to the file

    Returns:
        int: The size of the file in bytes
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return os.path.getsize(file_path)


def format_size(size: int) -> str:
    """
    Format a file size in bytes to a human-readable format.

    Args:
        size (int): The size of the file in bytes

    Returns:
        str: The formatted file size
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffix_index = 0
    while size > 1024 and suffix_index < len(suffixes) - 1:
        size /= 1024
        suffix_index += 1
    return f"{size:.2f} {suffixes[suffix_index]}"
