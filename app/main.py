from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class TitleRequest(BaseModel):
    title: str

@app.get("/")
async def root():
    return { "message" : "Welcome to HowItEnds API!" }

@app.post("/check-ending")
async def check_ending(request: TitleRequest):
    title = request.title
    prompt = os.getenv("AI_PROMPT").format(title=title)

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )

    ending = response.output_text.strip().lower()
    return {"title":  title, "ending": ending}


