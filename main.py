import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from groq import Groq
import asyncio
from dotenv import load_dotenv
import uvicorn


load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/chat")
async def chat(payload: dict):
    user_msg = payload["message"]

    async def token_stream():
        stream = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": user_msg}],
        stream=True
        )
        
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
                await asyncio.sleep(0)

    return StreamingResponse(token_stream(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)