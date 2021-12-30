import discord
from discord.ext import commands
import dao
from dao.data import get_stations
from output import messenger, player
from dto.models import RadioStation
import random


class Radio(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    # Commands
    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)

        if not ctx.message.author.voice:
            await messenger.send_message(
                ctx, f"You need to be in a voice channel {ctx.message.author.display_name}!"
            )
            return

        voice_client = await player.connect_to_voice(ctx, self.client)

        station = get_station(query)

        await messenger.send_playing_message(ctx, station)

        player.play_radio_station(voice_client, station)

    @commands.command()
    async def stop(self, ctx):
        await player.disconnet_from_voice(ctx)


def setup(client):
    client.add_cog(Radio(client))


def get_station(query) -> RadioStation:
    if dao.is_genre(query):
        return random.choice(dao.search_genres(query))

    if query.lower() == "random":
        return random.choice(dao.get_stations())

    return dao.search_stations(query)[0]
