from typing import Optional

from pydantic import BaseModel


class LyricsItem(BaseModel):
    artist: str
    album: str
    year: str
    title: str
    lyrics: Optional[str]
