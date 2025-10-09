from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.get("/")
async def root():
    return { "message" : "Welcome to HowItEnds API!" }

@app.post("/check-ending")
async def check_ending(movie: dict):
    title =movie["title"]
    prompt = os.getenv("AI_PROMPT").format(title=movie["title"])

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )

    ending = response.output_text.strip().lower()
    return {"title":  title, "ending": ending}