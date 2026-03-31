from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class MusicServer:
    id: str
    name: str
    url: str
    type: Literal["jellyfin", "navidrome"]
    token: str
    username: str

@dataclass
class Song:
    id: str
    title: str
    artist: str
    album: str
    duration: int  # em segundos
    stream_url: str
    cover_url: Optional[str] = None
    track_number: Optional[int] = None

@dataclass
class Album:
    id: str
    title: str
    artist: str
    year: Optional[int] = None
    cover_url: Optional[str] = None