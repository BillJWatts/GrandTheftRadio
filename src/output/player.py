"""Module containing all audio playback logic"""
import asyncio
import logging
from datetime import datetime

import discord
from discord.ext.commands import Context
from dto.models import RadioStation
from mutagen.mp3 import MP3

AUDIO_DIR = "src/resources/audio/"


async def connect_to_voice(context: Context, client: discord.Client) -> discord.VoiceClient:
    """Connects the client to the voice channel given in the context. If the client is already in
    a voice channel, then the client will be moved to the new channel.

    Args:
        context (Context): Context of the user command
        client (discord.Client): Client connection with discord

    Returns:
        discord.VoiceClient: Returns the newly connected voice client.
    """
    channel = context.message.author.voice.channel
    voice = discord.utils.get(context.guild.voice_channels, name=channel.name)
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=context.guild)

    if not voice_client:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)
    return voice_client


async def disconnect_from_voice(context: Context):
    """Disconnect from the voice client of given context. Will only disconnect bot if user is in the
    same voice channel.

    Args:
        context (Context): Context of the user command.
    """
    voice_client = context.message.guild.voice_client
    voice_client.stop()
    logging.info("Disconnecting from voice channel")
    await voice_client.disconnect()


async def play_radio_station(voice_client: discord.VoiceClient, station: RadioStation):
    """Outputs audio of the given radio station to the given voice client. Audio is looped until
    the stop command is given or a different radio station is played.

    Args:
        voice_client (discord.VoiceClient): Voice client which the audio source will be played over.
        station (RadioStation): Radio station which will be played.
    """
    if voice_client.is_playing():
        voice_client.stop()

    # Audio file length in seconds
    station_duration: int = _get_station_duration(station)

    while True:
        audio_timestamp = _get_live_timestamp(station)
        radio_source = discord.FFmpegPCMAudio(
            source=f"{AUDIO_DIR}{station.audio_file}",
            before_options=f"-ss {audio_timestamp}",
        )
        logging.info(f"Playing '{station.name}' at timestamp: {audio_timestamp} seconds")
        voice_client.play(source=radio_source)

        await asyncio.sleep((station_duration - audio_timestamp) + 1)

        if not voice_client.is_connected() or voice_client.is_playing():
            logging.info(f"Breaking {station.name} audio loop")
            break


def _get_station_duration(station: RadioStation) -> int:
    """Retrieve the length (seconds) of the mp3 audio file associated with the given radio station.

    Args:
        station (RadioStation): Radio station

    Returns:
        int: Lenght of the associated mp3 file in seconds.
    """
    return MP3(f"{AUDIO_DIR}{station.audio_file}").info.length


def _get_live_timestamp(station: RadioStation) -> int:
    """Calculates the current live timestamp of a radio station. Calculation assumes the radio has
    been playing on loop from midnight of the current day. Timestamp is given in seconds.

    Args:
        station (RadioStation): Radio station

    Returns:
        int: Returns the number of seconds after the start of the audio file.
    """
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_today = (now - midnight).seconds
    station_duration = _get_station_duration(station)
    return round(seconds_today % station_duration)
