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
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 400px;
                text-align: center;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
            }
            textarea, input {
                width: calc(100% - 22px);
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
            #response {
                margin-top: 20px;
                font-size: 14px;
                color: #333;
                word-wrap: break-word;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chat with GPT</h1>
            <textarea id="prompt" rows="4" placeholder="Enter your prompt here..."></textarea><br>
            <input type="number" id="max_tokens" value="50" min="1" max="100"><br>
            <button onclick="generateText()">Generate</button>
            <p id="response"></p>
        </div>

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