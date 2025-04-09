import os
import google.generativeai as genai
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings for a text using Gemini API."""
    try:
        embedding_model = "embedding-001"
        embedding = genai.embed_content(
            model=embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return embedding["embedding"]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise e

async def batch_generate_embeddings(chunks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Generate embeddings for multiple chunks."""
    embeddings = []
    
    for chunk in chunks:
        try:
            embedding = await generate_embeddings(chunk["content"])
            embeddings.append({
                **chunk,
                "embedding": embedding
            })
        except Exception as e:
            print(f"Error generating embedding for chunk from {chunk['fileName']}: {e}")
    
    return embeddings
