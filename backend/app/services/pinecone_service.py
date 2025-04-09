import os
from pinecone import Pinecone, ServerlessSpec
import asyncio
from typing import List, Dict, Any
import uuid
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone client globally
api_key = ""
print("API KEY:", api_key)
pc = Pinecone(api_key=api_key)

async def init_index():
    global pc
    
    print(api_key)
    if not api_key:
        print("\033[91mError: PINECONE_API_KEY environment variable not set\033[0m")
        print("\033[93mPlease set your Pinecone API key in the .env file:\033[0m")
        print("PINECONE_API_KEY=your_pinecone_api_key_here")
        sys.exit(1)
    
    try:

        
        index_name = os.getenv("PINECONE_INDEX_NAME", "law-assistant")
        dimension = int(os.getenv("EMBEDDING_DIMENSION", "1536"))  # OpenAI uses 1536 dimensions
        
        # Check if index exists
        try:
            indexes = pc.list_indexes().names()
            if index_name not in indexes:
                # Create index if it doesn't exist
                pc.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud=os.getenv("PINECONE_CLOUD", "aws"),
                        region=os.getenv("PINECONE_REGION", "us-east-1")
                    )
                )
                print(f"Created new Pinecone index: {index_name}")
            
            # Get the index
            return pc.Index(index_name)
            
        except Exception as e:
            if "Invalid API Key" in str(e):
                print("\033[91mError: Invalid Pinecone API Key\033[0m")
                print("\033[93mPlease check your Pinecone API key in the .env file\033[0m")
                sys.exit(1)
            else:
                print(f"\033[91mError initializing Pinecone index: {str(e)}\033[0m")
                raise
            
    except Exception as e:
        print(f"\033[91mError connecting to Pinecone: {str(e)}\033[0m")
        raise

async def store_embeddings(embeddings: List[Dict[str, Any]]):
    index = await init_index()
    
    # Batch upsert to Pinecone
    records = []
    
    # Check embedding dimensions from the first embedding
    if embeddings and "embedding" in embeddings[0]:
        embedding_dim = len(embeddings[0]["embedding"])
        print(f"Embedding dimension: {embedding_dim}")
        
        # Get index stats to check configured dimension
        index_stats = pc.describe_index(os.getenv("PINECONE_INDEX_NAME", "law-assistant"))
        index_dim = index_stats.dimension
        print(f"Index dimension: {index_dim}")
        
       
        index_name = os.getenv("PINECONE_INDEX_NAME", "law-assistant")
        index = pc.Index(index_name)
    
    for emb in embeddings:
        # Generate an ID if one doesn't exist
        emb_id = emb.get("id", str(uuid.uuid4()))
        
        # Handle embedding format - ensure we have a list of float values
        # OpenAI embeddings are already a list of floats from the generate_embeddings function
        embedding_values = emb["embedding"]
        
        record = {
            "id": emb_id,
            "values": embedding_values,
            "metadata": {
                "text": emb.get("content", ""),  # Store the content as text in metadata
                "fileName": emb.get("fileName", ""),
                "filePath": emb.get("filePath", ""),
                "source": emb.get("source", "")
            }
        }
        records.append(record)
    
    # Use the new upsert method
    if records:
        index.upsert(vectors=records)
    return len(records)

async def query_embeddings(query_vector, top_k=5):
    index = await init_index()
    
    # Query the index
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    
    return results
