import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import glob
from contextlib import asynccontextmanager

from backend.app.services.openai_service import generate_embeddings, generate_response
from backend.app.services.pinecone_service import store_embeddings, query_embeddings
from utils.document_processor import chunk_text

# Define lifespan context manager to replace on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the application by loading and processing documents
    print("Starting document processing...")
    await load_and_process_documents()
    print("Document processing completed!")
    yield
    # Shutdown: Clean up resources if needed
    print("Shutting down application...")

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

async def process_markdown_file(file_path):
    """Process a markdown file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

async def load_and_process_documents():
    """Load all markdown files from model/data directory and process them."""
    data_dir = "../model/data"
    os.makedirs(data_dir, exist_ok=True)
    markdown_files = glob.glob(os.path.join(data_dir, "*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {data_dir}")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process.")
    
    all_embedded_chunks = []
    
    for file_path in markdown_files:
        print(f"Processing {file_path}")
        # Read markdown file
        content = await process_markdown_file(file_path)
        if not content:
            continue
        
        # Chunk the text
        chunks = chunk_text(content)
        
        # Generate embeddings for each chunk using OpenAI
        file_name = os.path.basename(file_path)
        for i, chunk in enumerate(chunks):
            # Call OpenAI embedding service
            embedding = await generate_embeddings(chunk)
            all_embedded_chunks.append({
                "fileName": file_name,
                "filePath": file_path,
                "content": chunk,
                "embedding": embedding
            })
    
    # Store all embeddings in Pinecone
    if all_embedded_chunks:
        await store_embeddings(all_embedded_chunks)
        print(f"Successfully processed {len(all_embedded_chunks)} chunks from {len(markdown_files)} files.")
    else:
        print("No content was processed.")

@app.post("/query")
async def query(request: QueryRequest):
    """Query the system with a question."""
    try:
        # Generate embedding for the query using OpenAI
        query_embedding = await generate_embeddings(request.query)
        
        # Search Pinecone for relevant chunks
        results = await query_embeddings(query_embedding, top_k=3)
        
        # Extract the content from the search results
        context = "\n\n".join([match["metadata"]["text"] for match in results["matches"]])
        
        # Generate response using OpenAI instead of Gemini
        response = await generate_response(request.query, context)
        
        return {
            "response": response,
            "sources": [
                {"fileName": match["metadata"].get("fileName", "Unknown"), 
                 "text": match["metadata"]["text"][:200] + "..."} 
                for match in results["matches"]
            ]
        }
    except Exception as e:
        print(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "API is running. Visit /docs for documentation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
