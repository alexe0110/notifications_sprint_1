import logging

LOG_FORMAT = (
    '{"asctime": "%(asctime)s", "levelname": "%(levelname)s",  "module": "%(module)s",  "message": "%(message)s"}'
)


logger = logging.getLogger()
logger.setLevel(logging.INFO)


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger.addHandler(console_handler)
