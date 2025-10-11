from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel



load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing — check your .env file")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class TitleRequest(BaseModel):
    title: str

@app.get("/")
async def root():
return { "message" : "Welcome to HowItEnds API!" }

@app.post("/check-ending")
async def check_ending(request: TitleRequest):
try: 
    title = request.title
                        prompt = os.getenv("AI_PROMPT").format(title=title)

 try:
        response = client.responses.create(
            model="gpt-4o",
            input=prompt
        )
    except Exception as e:
        #any error like network/auth, timeout etc.
        raise HTTPException(status_code = 503, detail=f"Open AI error{type(e).__name__}")

    ending = response.output_text.strip().lower()
    return {"title":  title, "ending": ending}


