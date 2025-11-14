from fastapi import APIRouter
from api.v1.endpoints import list_tracks_by_artist

v1_router = APIRouter()

v1_router.include_router(list_tracks_by_artist.router, prefix="/list_tracks", tags=["list_tracks"])