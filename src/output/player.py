import asyncio
import logging
from datetime import datetime

import discord
from discord import FFmpegPCMAudio, VoiceClient
from discord.errors import ClientException
from dto.models import RadioStation
from mutagen.mp3 import MP3

AUDIO_DIR = "src/resources/audio/"


async def connect_to_voice(ctx, client):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice_client:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)
    return voice_client


async def disconnet_from_voice(ctx):
    voice_client = ctx.message.guild.voice_client
    voice_client.stop()
    await voice_client.disconnect()


async def play_radio_station(voice_client: VoiceClient, station: RadioStation):
    if voice_client.is_playing():
        voice_client.stop()

    station_duration = _get_station_duration(station)

    while True:
        audio_timestamp = _get_live_timestamp(station)
        radio_source = FFmpegPCMAudio(
            source=f"{AUDIO_DIR}{station.sid}.mp3",
            before_options=f"-ss {audio_timestamp}",
        )
        voice_client.play(source=radio_source)

        await asyncio.sleep((station_duration - audio_timestamp) + 1)

        if not voice_client.is_connected() or voice_client.is_playing():
            break


def _get_station_duration(station: RadioStation) -> int:
    return MP3(f"{AUDIO_DIR}{station.sid}.mp3").info.length


def _get_live_timestamp(station: RadioStation) -> int:
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_today = (now - midnight).seconds
    station_duration = _get_station_duration(station)
    return seconds_today % station_duration
