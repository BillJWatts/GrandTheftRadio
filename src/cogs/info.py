from discord.ext import commands
import dao
from output import messenger
import logging


class Info(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def list_genres(self, ctx):
        await messenger.send_embed(
            channel=ctx,
            title="Genres",
            description="\n".join(dao.get_genres()),
        )

    @commands.command()
    async def search(self, ctx, *args):
        search_results = dao.search_stations(" ".join(args))
        await messenger.send_search_result(ctx, search_results)

    @commands.command()
    async def search_genres(self, ctx, query):
        search_results = dao.search_genres(query)
        await messenger.send_search_result(ctx, search_results)

    @commands.command()
    async def all_stations(self, ctx):
        await messenger.send_embed(
            channel=ctx,
            title="GTA Radio Stations",
            url="https://gta.fandom.com/wiki/Radio_Stations",
            description="_All stations supported_",
        )


def setup(client):
    client.add_cog(Info(client))
