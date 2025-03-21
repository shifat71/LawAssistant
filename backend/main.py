from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", ""),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="qwen1.5-14b-chat",
            messages=[
                {"role": "system", "content": "You are an intelligent Law adviser. It is your prime and suprime duty to make people aware of their rights and duties under the respective country. You must guide them honestly and fairly"},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        assistant_response = response.choices[0].message.content
        print("ChatGPT: ", assistant_response.strip("\n").strip())
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 


    