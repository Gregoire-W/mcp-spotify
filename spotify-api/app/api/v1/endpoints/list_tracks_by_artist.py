from fastapi import APIRouter, Depends
from app.core.spotify_client import SpotifyClient, get_spotify_client
from app.schema.spotify_api_schemas import ListTracksRequest

router = APIRouter()

@router.post("/", summary="")
async def list_tracks_by_artist(
    request: ListTracksRequest,
    spotifyClient: SpotifyClient = Depends(get_spotify_client)
):
    artist_name = request.artist_name
    data = spotifyClient.get(endpoint=f"v1/search?q={artist_name}&type=artist&limit=1")

    if (not data["artists"]["items"] or len(data["artists"]["items"]) == 0):
        raise ValueError(f"Artist '{artist_name}' not found")

    artist = data["artists"]["items"][0]
    
    top_tracks_data = spotifyClient.get(endpoint=f"v1/artists/{artist['id']}/top-tracks?market=US")

    return {
        "artist": {
            "id": artist["id"],
            "name": artist["name"],
            "image": artist["images"][0]["url"],
            "followers": artist["followers"]["total"],
            "genres": artist["genres"],
        },
        "tracks": [
            {
                "id": track["id"],
                "name": track["name"],
                "album": track["album"]["name"],
                "albumImage": track["album"]["images"][0]["url"],
                "duration": track["duration_ms"],
                "popularity": track["popularity"],
                "previewUrl": track["preview_url"],
                "spotifyUrl": track["external_urls"]["spotify"],
            } for track in top_tracks_data["tracks"]
        ]
    }
