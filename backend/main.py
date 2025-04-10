import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import glob
from contextlib import asynccontextmanager

# Fix imports to use relative paths instead of absolute paths
from utils.openai_service import generate_embeddings, generate_response
from utils.pinecone_service import store_embeddings, query_embeddings
from utils.document_processor import chunk_text

# Define FastAPI app with lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Process documents
    print("Starting document processing...")
    await load_and_process_documents()
    print("Document processing completed!")
    yield
    # Shutdown: Clean up resources
    print("Shutting down application...")

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of your FastAPI application code ...
