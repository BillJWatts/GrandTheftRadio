import json
from typing import List
from fuzzywuzzy import fuzz, process
from dto.models import RadioStation
import logging

STATION_LIST: List[RadioStation] = None


def get_stations() -> List[RadioStation]:

    if STATION_LIST:
        return STATION_LIST

    with open("src/resources/radio_stations.json") as station_data:
        return json.loads(station_data.read(), object_hook=_decode_station)


def search_stations(query: str) -> List[RadioStation]:

    stations = get_stations()

    if query.isnumeric():
        return _search_by_id(int(query), stations)

    stations.sort(key=lambda station: fuzz.ratio(query, station.name), reverse=True)
    results = stations[:5]

    logging.info(f"Search results: {results}")

    return results


def get_genres() -> List[str]:
    stations = get_stations()
    genres = set()
    for station in stations:
        genres.update(station.genres)
    return sorted(list(genres))


def search_genres(query: str) -> List[RadioStation]:
    stations = get_stations()
    stations = [station for station in stations if _genre_match(query, station.genres)]
    return stations


def is_genre(query: str) -> bool:
    return _genre_match(query, get_genres())


def _genre_match(query: str, genres: List[str]) -> bool:
    return process.extractOne(query, genres)[1] > 80


def _search_by_id(sid: int, station_list: List[RadioStation]):
    for station in station_list:
        if station.sid == sid:
            return [station]


def _decode_station(station: dict) -> List[RadioStation]:
    return RadioStation(station["name"], station["genres"], station["game"], station["sid"])
