# encoding=utf-8
import logging
from typing import Any, Optional

from .utils import logdir_checker


class Logger:

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(
        self,
        lvl: Optional[Any] = INFO,
        filepath: Optional[str] = "./logs/log.log",
        filemode: Optional[str] = "a",
        encoding: Optional[str] = "utf-8",
    ):
        logdir_checker()
        self.logging = logging
        file_handler = logging.FileHandler(filepath, filemode, encoding)
        file_handler.setLevel(lvl)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(module)s:%(name)s:%(lineno)s - %(levelname)s - %(message)s"
            )
        )
        self.logging.basicConfig(
            level=lvl,
            format="-> %(levelname)s: %(message)s",
            encoding=encoding,
            handlers=[file_handler, logging.StreamHandler()],
        )

    def log(self, msg, lvl: Optional[Any] = DEBUG):
        return self.logging.log(lvl, msg)
