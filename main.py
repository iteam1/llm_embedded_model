import os
import uvicorn
from openai import OpenAI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse


# Init
LLM_MODEL = 'gpt-3.5-turbo'

# Create instance
app = FastAPI()
client = OpenAI()

class OpenAIRequest(BaseModel):
    prompt: str
    max_tokens: int = 50

@app.post("/generate")
async def generate_text(request: OpenAIRequest):
    try:
        response = client.chat.completions.create(
            model = LLM_MODEL,
            messages = [{'role':'user','content':request.prompt}],
            max_tokens = request.max_tokens,
            temperature = 0)

        return {'text':response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve the chat UI
@app.get("/")
async def get_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat UI</title>
    </head>
    <body>
        <h1>Chat with GPT</h1>
        <textarea id="prompt" rows="4" cols="50" placeholder="Enter your prompt here..."></textarea><br>
        <input type="number" id="max_tokens" value="50"><br>
        <button onclick="generateText()">Generate</button>
        <p id="response"></p>

        <script>
            async function generateText() {
                const prompt = document.getElementById("prompt").value;
                const max_tokens = document.getElementById("max_tokens").value;
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: prompt, max_tokens: parseInt(max_tokens) })
                });

                const data = await response.json();
                document.getElementById("response").innerText = data.text;
            }
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)