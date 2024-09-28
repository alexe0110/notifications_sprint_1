import logging
import os
from pathlib import Path

LOG_FORMAT = (
    '{"asctime": "%(asctime)s", "levelname": "%(levelname)s",  "module": "%(module)s",  "message": "%(message)s"}'
)


def get_file_handler(path: str) -> logging.FileHandler:
    path_dir = Path(path).parent
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)

    return logging.FileHandler(path)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = get_file_handler('/opt/app/event_generator/logs/app.log')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger.addHandler(file_handler)
logger.addHandler(console_handler)
