from datetime import datetime

import discord
from discord import FFmpegPCMAudio, VoiceClient
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


def play_radio_station(voice_client: VoiceClient, station: RadioStation):
    if voice_client.is_playing():
        voice_client.stop()

    radio_source = FFmpegPCMAudio(
        f"{AUDIO_DIR}{station.sid}.mp3",
        executable="C:\\FFmpeg\\bin\\ffmpeg.exe",
        before_options=f"-ss {_get_live_timestamp(station)}",
    )
    voice_client.play(radio_source)


def _get_live_timestamp(station: RadioStation) -> int:
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_today = (now - midnight).seconds
    audio = MP3(f"{AUDIO_DIR}{station.sid}.mp3")
    seconds = audio.info.length
    return seconds_today % seconds
