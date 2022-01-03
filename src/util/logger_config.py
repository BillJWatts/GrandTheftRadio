"""Module containing logging configuration details"""
import logging

FILENAME = "bot.log"
FORMAT = "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
LEVEL = logging.DEBUG


def set_logging_config():
    logging.basicConfig(
        filename=FILENAME,
        filemode="w",
        format=FORMAT,
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=LEVEL,
    )
