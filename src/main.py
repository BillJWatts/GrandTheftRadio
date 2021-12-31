import logging
from pathlib import Path
from resources.auth import TOKEN
from discord.ext import commands

logging.basicConfig(filename="bot.log", filemode="w", encoding="utf-8", level=logging.DEBUG)
COGS_PATH = Path("src/cogs")

client = commands.Bot(command_prefix="gtr.")


@client.event
async def on_ready():
    logging.info(f"Succesfully logged in as {client.user}")


@client.command()
async def load(ctx, extension: str):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} extension loaded!")


@client.command()
async def unload(ctx, extension: str):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} extension unloaded!")


@client.command()
async def reload(ctx, extension: str):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} extension reloaded!")


if __name__ == "__main__":

    for file in COGS_PATH.iterdir():
        if file.suffix == ".py":
            client.load_extension(f"cogs.{file.stem}")

    client.run(TOKEN)
