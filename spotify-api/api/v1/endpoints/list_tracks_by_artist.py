import requests
from fastapi import APIRouter, Depends
from core.spotify_client import SpotifyClient, get_spotify_client

router = APIRouter()

@router.post("/", summary="")
def list_tracks_by_artist(
    artist_name: str,
    spotifyClient: SpotifyClient = Depends(get_spotify_client)
):
    access_token = spotifyClient.get_token()

    response = requests.post(
        url=f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1",
        headers={
            "Authorization": f"Bearer {access_token}",
        }
    )

    if (not response["ok"]):
        raise ValueError(f"Failed to search artist: {response['statusText']}")

    data = response.json()

    if (not data["artists"]["items"] or len(data["artists"]["items"]) == 0):
        raise ValueError(f"Artist '{artist_name}' not found")

    artist = data["artists"]["items"][0]

    response = requests.post(
        url=f"https://api.spotify.com/v1/artists/{artist.id}/top-tracks?market=US",
        headers={
            "Authorization": f"Bearer {access_token}",
        }
    )

    if (not response["ok"]):
        raise ValueError(f"Failed to get top tracks: {response['statusT ext']}")
    
    top_tracks_data = response.json()

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
