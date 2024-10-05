import logging
from types import MappingProxyType
from typing import Literal

LEVELS = MappingProxyType({
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
})

LOG_LEVELS = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class ColorfulFormatter(logging.Formatter):
    """
    ColorfulFormatter class for logging
    """
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[91m',  # Red
    }

    RESET = '\033[0m'

    def __init__(self, app_name: str):
        super().__init__()
        self.app_name = app_name

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = f"{color}[{self.app_name}] {record.levelname}{self.RESET}: {record.msg}"  # noqa
        return f'{message}'


def setup_logger(app_name: str, debug_level: LOG_LEVELS = 'DEBUG') -> logging.Logger:
    """
    This function sets up the logger for the application
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = ColorfulFormatter(app_name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if debug_level in LEVELS:
        logger.setLevel(LEVELS[debug_level])
    else:
        raise ValueError(f"Invalid log level: {debug_level}")

    return logger
