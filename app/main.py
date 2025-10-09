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
    prompt = f"Return only one word happy sad bittersweet or ambiguous that best describes the overall ending of the {title} It could be a movie series anime or book Do not include any explanation or extra text If information about the ending is not found in existing data search the web for reliable summaries before responding"

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )

    ending = response.output_text.strip().lower()
    return {"title":  title, "ending": ending}