#!/usr/bin/env python
"""Entry point for the discord bot"""
import logging
import os
from util.logger_config import set_logging_config
from pathlib import Path
from discord.ext import commands


if __name__ == "__main__":

    set_logging_config()

    COGS_PATH = Path("src/cogs")
    DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")

    if DISCORD_API_TOKEN is None:
        print("ERROR: 'DISCORD_API_TOKEN' must be set as an environment " \
              "variable")
        exit(os.EX_NOINPUT)

    client = commands.Bot(command_prefix="gtr.")

    @client.event
    async def on_ready():
        logging.info(f"Succesfully logged in as {client.user}")

    # Load all cogs (modules)
    for file in COGS_PATH.iterdir():
        if file.suffix == ".py":
            client.load_extension(f"cogs.{file.stem}")

    # Start the bot
    client.run(DISCORD_API_TOKEN)
