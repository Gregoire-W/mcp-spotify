import os
import requests
import time
from typing import Optional
from fastapi import HTTPException

class SpotifyClient():

    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID", None)
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", None)

        if self.client_id is None:
            assert ValueError("Client ID should be defined as an environment variable")
        elif self.client_secret  is None:
            assert ValueError("Client secret should be defined as an environment variable")
        self.token = None
        self.expire = None

    def _is_token_valid(self):
        return self.expire is None or self.expire < time.time() 
    
    def _fetch_new_token(self):
        if self._is_token_valid():
            response = requests.post(
                url="https://accounts.spotify.com/api/token",
                headers= {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }
            )
        return response

    def get_token(self):
        if self._is_token_valid():
            response = self._fetch_new_token()

            data = response.json()
            self.token = data["access_token"]
            self.expire = time.time() + int(data["expires_in"]) - 30 # Get a 30 seconds threshold on expiration time

        return self.token
    
    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        token = self.get_token()
        url = f"https://api.spotify.com/{endpoint}"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=response.status_code if hasattr(response, 'status_code') else 500,
                detail=f"Erreur lors de l'appel à l'API Spotify: {str(e)}"
            )        


_spotify_client: Optional[SpotifyClient] = None

def get_spotify_client() -> SpotifyClient:
    global _spotify_client
    if _spotify_client is None:
        _spotify_client = SpotifyClient()  # ← Créé UNE SEULE FOIS
    return _spotify_client  # ← Retourne toujours la même instance