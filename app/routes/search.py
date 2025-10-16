from fastapi import APIRouter, Query, HTTPException
from dotenv import load_dotenv
from app.routes import search, ending
import requests
import os


load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
router = APIRouter()


@router.get("/search")
async def routes( q: str, limit: int = 12):
    url ="https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key" : TMDB_API_KEY,
        "query" : q,
        "include_adult": "true",
        "language": "en_US",
        "page": 1
    }

    response = requests.get(url, params=params, timeout=5)
    if response.status_code != 200:
        raise HTTPException(status_code = 502, detail="TMDb request failed")

    data = response.json()

    results = []
    for item in data.get("results", []):
        if item.get("media_type") == "person":
            continue
        title = item.get("title") or item.get("name")
        if not title:
            continue
        date = item.get("release_date") or item.get("first_air_date") or ""
        year = date[:4] if len(date) >= 4 else None
        poster_path = item.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w342{poster_path}" if poster_path else None
        results.append({
            "id": item.get("id"),
            "media_type": item.get("media_type"),
            "title": title,
            "year": year,
            "poster_url": poster_url
        })
        if len(results) >= limit:
            break

    return {"query": q, "results": results}



