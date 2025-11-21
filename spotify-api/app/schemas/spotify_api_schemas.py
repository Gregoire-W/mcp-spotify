from pydantic import BaseModel

class ListTracksRequest(BaseModel):
    artist_name: str

class CreatePlaylistRequest(BaseModel):
    name: str
    desc: str
    public: bool = False