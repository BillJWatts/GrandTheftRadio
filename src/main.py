"""Entry point for the discord bot"""
import logging
from util.logger_config import set_logging_config
from pathlib import Path
from resources.auth import TOKEN
from discord.ext import commands


if __name__ == "__main__":

    set_logging_config()

    COGS_PATH = Path("src/cogs")

    client = commands.Bot(command_prefix="gtr.")

    @client.event
    async def on_ready():
        logging.info(f"Succesfully logged in as {client.user}")

    # Load all cogs (modules)
    for file in COGS_PATH.iterdir():
        if file.suffix == ".py":
            client.load_extension(f"cogs.{file.stem}")

    # Start the bot
    client.run(TOKEN)
