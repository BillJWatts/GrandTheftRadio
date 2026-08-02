#!/usr/bin/env python
"""Entry point for the discord bot"""

import logging
import os
from util.logger_config import set_logging_config
from pathlib import Path
from discord.ext import commands
import discord
import asyncio

COGS_PATH = Path("src/cogs")


async def main():
    set_logging_config()
    api_token = _get_api_token()
    bot = _create_bot()

    @bot.event
    async def on_ready():
        logging.info(f"Succesfully logged in as {bot.user}")

    await _load_cogs(bot)

    # Start the bot
    await bot.start(api_token)


async def _load_cogs(bot: commands.Bot):
    """Loads all cogs present in the cogs directory"""

    # Load all cogs (modules)
    for file in COGS_PATH.iterdir():
        if file.suffix == ".py":
            await bot.load_extension(f"cogs.{file.stem}")


def _get_api_token() -> str:
    """Retrieves discord api authentication token from environment variables"""

    api_token = os.getenv("GTR_DISCORD_API_TOKEN")

    if not api_token:
        print(
            "ERROR: 'GTR_DISCORD_API_TOKEN' must be set as an environment " "variable"
        )
        exit()

    return api_token


def _create_bot() -> commands.Bot:
    """Creates discord bot with message_content event subscription

    Returns:
        commands.Bot: Discord bot
    """
    # Intents are event subscriptions, we only need to monitor message events
    intents = discord.Intents.default()
    intents.message_content = True

    return commands.Bot(command_prefix="gtr.", intents=intents)


if __name__ == "__main__":
    asyncio.run(main())
