"""Module containing all message sending logic"""
from typing import List
from dto.models import RadioStation
from discord.ext.commands import Context
import discord
import logging


async def send_message(channel, message: str):
    await channel.send(message)


async def send_embed(channel, title: str, description: str = "", url: str = ""):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.url = url
    await channel.send(embed=embed)


async def send_search_result(channel, station_list: List[RadioStation]):
    if station_list:
        message = _format_station_list(station_list)
    else:
        message = "No stations found"
    await send_embed(channel=channel, title="Search Results", description=message)


async def send_playing_message(channel, station: RadioStation):
    await send_message(channel, "Now playing:")
    await send_embed(
        channel=channel,
        title=station.name,
        description=station.game,
        url=f"https://gta.fandom.com/wiki/{station.name.replace(' ', '_')}",
    )


def _format_station_list(stations: List[RadioStation]) -> str:
    """Formats a list of RadioStation objects into a readable message string

    Args:
        stations (List[RadioStation]): list of RadioStation objects
    Returns:
        str: formatted message string
    """
    stations.sort(key=lambda x: x.game)

    current_game = stations[0].game
    station_list = f"**{current_game}**\n"

    for station in stations:
        if station.game != current_game:
            current_game = station.game
            station_list += f"\n**{current_game}**\n"
        station_list += f"{station}\n"

    return station_list
