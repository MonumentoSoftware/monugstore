# Command line interface for reading a json file and dumping it on a string.
# It accepts a file path as an argument.
#

import json
import sys

from monugstore.utils.json_io import read_json
from monugstore.utils.logging import setup_logger

logger = setup_logger(__name__)


def dump_json(file_path: str) -> str:
    """
    Read a JSON file and dump it on a string.

    Args:
        file_path (str): The path to the JSON file

    Returns:
        str: The JSON string
    """
    data = read_json(file_path)
    return json.dumps(data)


def main():
    if len(sys.argv) != 2:
        logger.error("Usage: dump-key <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(dump_json(file_path))


if __name__ == "__main__":
    main()
