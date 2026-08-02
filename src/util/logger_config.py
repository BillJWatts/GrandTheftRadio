"""Module containing logging configuration details"""

import logging
import sys

FILENAME = "bot.log"
FORMAT = "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
LEVEL = logging.DEBUG


def set_logging_config():
    file_handler = logging.FileHandler(FILENAME, mode="w", encoding="utf-8")
    stdout_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        format=FORMAT,
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=LEVEL,
        handlers=[file_handler, stdout_handler],
    )