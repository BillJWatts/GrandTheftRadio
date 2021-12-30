from typing import Any, List
from dataclasses import dataclass


@dataclass
class RadioStation:
    name: str
    genres: List[str]
    game: str
    sid: str

    def __str__(self):
        return f"{self.name} - _{', '.join(self.genres)}_ - [{self.sid}]"
