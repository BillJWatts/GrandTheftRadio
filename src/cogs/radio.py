"""Module containing all radio (audio playback) user commands"""
from typing import List
from discord.ext import commands
from dao import data
from output import messenger, player
from dto.models import RadioStation, SearchQuery
import random


class Radio(commands.Cog):
    """Radio commands. Allows the user to play gta radio stations through a voice channel"""

    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def play(self, context: commands.Context, *args):
        """Play a station best matching a query. User can input a name, genre or sid

        #TODO Allow user to enter a game title

        Args:
            context ([type]): Context of the user command
            args (List[str]): Search query
        """

        # Check if user is in a voice channel
        if not context.message.author.voice:
            await messenger.send_message(
                context, f"You need to be in a voice channel {context.message.author.display_name}!"
            )
            return

        voice_client = await player.connect_to_voice(context, self.client)

        station = self._get_station(SearchQuery(args))

        await messenger.send_playing_message(context, station)

        await player.play_radio_station(voice_client, station)

    @commands.command()
    async def stop(self, context: commands.Context):
        """Stop the radio from playing audio and disconnects bot from the voice channel

        Args:
            context (commands.Context): Context of the user command
        """
        await player.disconnect_from_voice(context)

    @staticmethod
    def _get_station(query: SearchQuery) -> RadioStation:
        """Retrieves a station best matching a search query

        XXX Logic here is very similar to data.search_stations() maybe combine

        Args:
            query (SearchQuery): query

        Returns:
            RadioStation: Radio station to be played
        """
        if query.is_sid():
            return data.search_by_sid(int(query))

        if query.is_genre():
            return random.choice(data.search_by_genre(str(query)))

        if query.is_game():
            return random.choice(data.search_by_game(str(query)))

        if str(query).lower() == "random":
            return random.choice(data.get_stations())

        # Return the best search result
        return data.search_stations(query)[0]


def setup(client):
    client.add_cog(Radio(client))
