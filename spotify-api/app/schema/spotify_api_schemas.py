from pydantic import BaseModel

class ListTracksRequest(BaseModel):
    artist_name: str