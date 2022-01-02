"""Module containing data retrieval logic"""
import json
from typing import List, Optional
from fuzzywuzzy import fuzz, process
from dto.models import RadioStation, MatchingResult, SearchQuery
import logging

STATION_LIST: List[RadioStation] = None


def get_stations() -> List[RadioStation]:
    """Retrieve station data from memory or json storage

    Returns:
        List[RadioStation]: Returns a list of all radio stations
    """

    def _decode_station(station: dict) -> RadioStation:
        """Decodes json data into a RadioStation object

        XXX Nested function 😠

        Args:
            station (dict): station data

        Returns:
            RadioStation
        """
        return RadioStation(station["name"], station["genres"], station["game"], station["sid"])

    # Grab from memory if already loaded
    global STATION_LIST
    if STATION_LIST:
        return STATION_LIST

    logging.info(f"Loading station data.")
    with open("src/resources/radio_stations.json") as station_data:
        station_list = json.loads(station_data.read(), object_hook=_decode_station)
        # Store in memory
        STATION_LIST = station_list
        return station_list


def search_stations(query: SearchQuery) -> List[RadioStation]:
    """Searches station data against a given search query.
    Query is first checked if it is a station id. Then is checked if it is a genre.
    If neither then a search is done against radio names using fuzzy matching and top 5 is returned.

    Args:
        query (SearchQuery)

    Returns:
        List[RadioStation]: List of radio stations found matching the query
    """
    if query.is_sid():
        logging.info(f"Searching stations by sid: '{query}'")
        return [search_by_sid(int(query))]

    if query.is_genre():
        logging.info(f"Searching stations by genre '{query}'")
        return search_by_genre(str(query))

    if query.is_game():
        logging.info(f"Searching stations by game '{query}'")
        return search_by_game(str(query))

    logging.info(f"Searching stations by name: '{query}'")
    matching_results: List[MatchingResult] = _match_stations(str(query))
    top_five_results = matching_results[:5]

    logging.info(f"Top search results: {top_five_results}")

    return [result.radio_station for result in top_five_results]


def search_by_sid(sid: int) -> Optional[RadioStation]:
    """Searches for a matching station id

    Args:
        sid (int): Station id query

    Returns:
        Optional[RadioStation]: RadioStation with matching sid or None if there is no match
    """
    for station in get_stations():
        if station.sid == sid:
            return station


def search_by_genre(genre: str) -> List[RadioStation]:
    """Searches for radio stations with a matching genre to the query.
    Attempts a fuzzy match against genres as well as an exact match
    exmaples :
        '80 pop' matches '80s pop'
        'pop' matches '80s pop'
        '80s pop' does not match 'pop'

    Args:
        query (str): genre query

    Returns:
        List[RadioStation]: List of radio stations with a matching genre
    """
    stations = [
        station
        for station in get_stations()
        if (_genre_match(genre, station.genres) or _has_genre(genre, station.genres))
    ]
    return stations


def search_by_game(game: str) -> List[RadioStation]:
    """Searches for radio stations with a matching game to the query.

    Args:
        game (str): game query

    Returns:
        List[RadioStation]: List of radio stations with a matching game
    """
    stations = [station for station in get_stations() if _game_match(game, station.game)]
    return stations


def get_genres() -> List[str]:
    """Retrieve all genres listed in the radio station data

    Returns:
        List[str]: List of unique genres
    """
    stations = get_stations()
    genres = set()
    for station in stations:
        genres.update(station.genres)
    return sorted(list(genres))


def get_games() -> List[str]:
    """Retrieve all games listed in the radio station data

    Returns:
        List[str]: List of unique games
    """
    stations = get_stations()
    games = set()
    for station in stations:
        games.add(station.game)
    return list(games)


def is_game(query: str) -> bool:
    """Checks if a query string is a game

    Args:
        query (str): potential game

    Returns:
        bool: true if the query is a match to a game
    """
    for game in get_games():
        if _game_match(query, game):
            return True
    return False


def is_genre(query: str) -> bool:
    """Checks if a query string is a genre

    Args:
        query (str): potential genre

    Returns:
        bool: True if query is a close match to a genre
    """
    return _genre_match(query, get_genres())


def _genre_match(query: str, genres: List[str]) -> bool:
    """Takes the best result of a fuzzy match against a list of genres and checks if the matching
    score is higher than 90%

    XXX Score threshold was arbitrarily chosen, needs testing

    Args:
        query (str): genre query
        genres (List[str]): list of genres to match against

    Returns:
        bool: True if at least one matching score is higher than 90%
    """
    _, best_score = process.extractOne(query, genres)
    if not best_score:
        return False
    return best_score > 90


def _game_match(query: str, game: str) -> bool:
    """Performs a fuzzy match between a query and game

    Args:
        query (str): potential game
        game (str): game

    Returns:
        bool: True if the matching score is larger than 90%
    """
    game = game.replace("Grand Theft Auto:", "")
    return fuzz.ratio(query.lower(), game.lower()) > 90


def _has_genre(query: str, genres: List[str]) -> bool:
    """Checks if the query string has an exact match or substring with one genre in the given genre list.

    Args:
        query (str): genre query
        genres (List[str]): list of genres to match against

    Returns:
        bool: True if a match is found
    """
    return any([query.lower() in genre.lower() for genre in genres])


def _match_stations(query: str) -> List[MatchingResult]:
    """Performs a fuzzy match of the query against all station names and returns sorted matching results

    XXX Inconsistent results noticed from this function, needs testing

    Args:
        query (str): station name query

    Returns:
        List[MatchingResult]: list of matching results
    """

    matching_results = [
        MatchingResult(
            radio_station=station, matching_score=fuzz.partial_ratio(query, station.name)
        )
        for station in get_stations()
    ]
    # Sort by matching score
    matching_results.sort(key=lambda result: result.matching_score, reverse=True)

    return matching_results
