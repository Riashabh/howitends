from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.routes import search, ending
from fastapi.middleware.cors import CORSMiddleware

import requests


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_PROMPT = os.getenv("AI_PROMPT")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing — check your .env file")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

class TitleRequest(BaseModel):
    title: str
    year: str | None = None

@app.get("/")
async def root():
    return {"message": "Welcome to HowItEnds API!"}


@app.post("/check-ending")
async def check_ending(request: TitleRequest):
    try:
        title = f"{request.title} ({request.year})" if request.year else request.title
        prompt = os.getenv("AI_PROMPT").format(title=title)

        response = client.responses.create(model="gpt-5", input=prompt)

        ending = response.output_text.strip().lower()
        return {"title": title, "ending": ending}

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"OpenAI error: {type(e).__name__}")



app.include_router(search.router)

