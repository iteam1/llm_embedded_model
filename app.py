import os
import uvicorn
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Init
LLM_MODEL = 'gpt-3.5-turbo'

# Create instance
app = FastAPI()
client = OpenAI()

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIRequest(BaseModel):
    prompt: str
    max_tokens: int = 50

@app.post("/generate")
async def generate_text(request: OpenAIRequest):
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=0
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)