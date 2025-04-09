import os
from openai import AsyncOpenAI 
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Get API key from .env file
api_key = ""
if not api_key:
    print("\033[91mError: OPENAI_API_KEY not found in environment variables\033[0m")
    print("\033[93mPlease add your OpenAI API key to the .env file:\033[0m")
    print("OPENAI_API_KEY=your_openai_api_key_here")
    sys.exit(1)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=api_key)

async def generate_embeddings(text):
    """Generate embeddings for the given text using OpenAI's embeddings API."""
    try:
        response = await client.embeddings.create(
            model="text-embedding-ada-002",  # This model outputs 1536-dimensional embeddings
            input=text,

        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        raise

async def generate_response(query, context):
    """Generate a response to the query using OpenAI's completions API."""
    try:
        system_prompt = """You are a legal assistant with expertise in law. 
        Use the provided legal context to answer the user's question accurately and concisely. 
        If the context doesn't contain relevant information to answer the question, say so clearly."""
        
        user_prompt = f"""Question: {query}
        
        Context:
        {context}
        
        Please provide a comprehensive answer based on the context provided."""
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo",  # or another appropriate model like gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        raise
