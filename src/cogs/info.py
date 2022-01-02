"""Module containing all info (radio data retrieval) user commands"""
from typing import List
from discord.ext import commands
from dao import data
from dto.models import SearchQuery
from output import messenger
import logging


class Info(commands.Cog):
    """Info commands. Allows the user to query or list all radio station data."""

    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def genres(self, context: commands.Context):
        """Lists all music genres available through grand theft radio

        Args:
            context (commands.Context): Context of the user command
        """
        await messenger.send_embed(
            channel=context,
            title="Genres",
            description="\n".join(data.get_genres()),
        )

    @commands.command()
    async def stations(self, context: commands.Context):
        """Lists all radio stations available through grand theft radio

        Args:
            context (commands.Context): Context of the user command
        """
        await messenger.send_embed(
            channel=context,
            title="GTA Radio Stations",
            url="https://gta.fandom.com/wiki/Radio_Stations",
            description="_All stations supported_",
        )

    @commands.command()
    async def search(self, context: commands.Context, *args):
        """Searches for radio stations by name, genre or id number

        TODO Allow user to enter a game title to retrieve all stations from that game

        Args:
            context (commands.Context): Context of the user command
            args (List[str]): Search query sent by user
        """
        search_results = data.search_stations(SearchQuery(args))
        await messenger.send_search_result(context, search_results)


def setup(client):
    client.add_cog(Info(client))
