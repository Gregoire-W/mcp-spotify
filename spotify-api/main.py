from dotenv import load_dotenv
from fastapi import FastAPI
from api.router import api_router

load_dotenv()

app = FastAPI(title="Spotify API", version="1.0.0")

app.include_router(api_router)