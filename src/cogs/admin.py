"""Module containing all admin commands"""
from discord.ext import commands
from output import messenger
import logging


class Admin(commands.Cog):
    """Admin commands for cog management"""

    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, context: commands.Context, extension: str):
        """Loads a cog file to the client

        Args:
            context (commands.Context): Context of the user command
            extension (str): cog extension to be loaded
        """
        await self.client.load_extension(f"cogs.{extension}")
        await messenger.send_message(context, f"{extension.capitalize()} extension loaded!")

    @commands.command()
    @commands.is_owner()
    async def unload(self, context: commands.Context, extension: str):
        """Unloads a cog file from the client

        Args:
            context (commands.Context): Context of the user command
            extension (str): cog extension to be unloaded
        """
        await self.client.unload_extension(f"cogs.{extension}")
        await messenger.send_message(context, f"{extension.capitalize()} extension unloaded!")

    @commands.command()
    @commands.is_owner()
    async def reload(self, context: commands.Context, extension: str):
        """Reloads a cog file to the client

        Args:
            context (commands.Context): Context of the user command
            extension (str): cog extension to be reloaded
        """
        await self.client.unload_extension(f"cogs.{extension}")
        await self.client.load_extension(f"cogs.{extension}")
        await messenger.send_message(context, f"{extension.capitalize()} extension reloaded!")


async def setup(client):
    await client.add_cog(Admin(client))
