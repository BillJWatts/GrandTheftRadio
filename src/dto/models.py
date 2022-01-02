"""Module containing all data objects used in the program"""
from typing import List, NamedTuple
from dataclasses import dataclass


@dataclass
class RadioStation:
    """Dataclass representing a Radio Station

    Attributes:
        name (str): Name of the radio station
        genres (List[str]): Genres of the station
        game (str): Game the station comes from
        sid (str): Station id
        audio_file (str)(Read only): Name of the audio file.
    """

    name: str
    genres: List[str]
    game: str
    sid: str

    @property
    def audio_file(self) -> str:
        """Gets the name of the audio file"""
        return f"{self.sid}.mp3"

    def __str__(self):
        return f"{self.name} - _{', '.join(self.genres)}_ - [{self.sid}]"


class MatchingResult(NamedTuple):
    """Namedtuple representing a fuzzy matching result"""

    radio_station: RadioStation
    matching_score: int


class SearchQuery:
    """Class representing a search query

    TODO add 'is_game' method

    Methods:
        is_sid: Returns true if query is an station id
        is_genre: Return true if query is a genre

    """

    def __init__(self, query: List[str]) -> None:
        self._query: str = " ".join(query)

    def is_sid(self) -> bool:
        return self._query.isnumeric()

    def is_genre(self) -> bool:

        # TODO Find a better way to avoid the circular import
        from dao import data

        return data.is_genre(self._query)

    def __str__(self) -> str:
        return self._query

    def __int__(self) -> int:
        return int(self._query)
