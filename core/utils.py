import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_LOG_DIR = "logs"
LOGDIR_PATH = os.path.join(BASE_DIR, BASE_LOG_DIR)


def logdir_exists() -> bool:
    return os.path.exists(LOGDIR_PATH)


def logdir_checker():
    if not logdir_exists():
        os.mkdir(LOGDIR_PATH)


def change_to_level(value, default_value):
    if value in logging._nameToLevel:
        return logging._nameToLevel[value]
    return int(default_value)
