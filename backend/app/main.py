from fastapi import FastAPI
from app.routers.router import router as demo_router
from app.routers.chatgpt import router as chat_router
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running. Visit /docs for documentation"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(chat_router)

app.include_router(demo_router)