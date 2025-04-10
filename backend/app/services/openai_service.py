import os
from openai import AsyncOpenAI 
from dotenv import load_dotenv
import sys
import tiktoken

# Load environment variables from .env file
load_dotenv()

# Get API key from .env file
api_key =""

if not api_key:
    print("\033[91mError: OPENAI_API_KEY not found in environment variables\033[0m")
    print("\033[93mPlease add your OpenAI API key to the .env file:\033[0m")
    print("OPENAI_API_KEY=your_openai_api_key_here")
    sys.exit(1)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=api_key)

# Initialize tokenizer for the embedding model
tokenizer = tiktoken.get_encoding("cl100k_base")  # Embedding model uses cl100k_base encoding

def count_tokens(text):
    """Count the number of tokens in a text string."""
    return len(tokenizer.encode(text))

def split_text(text, max_tokens=4000):
    """Split text into chunks that won't exceed the token limit."""
    if count_tokens(text) <= max_tokens:
        return [text]
    
    # Split by paragraphs first
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed the limit, save current chunk and start new one
        if count_tokens(current_chunk + paragraph) > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # If the paragraph itself is too large, split it by sentences
            if count_tokens(paragraph) > max_tokens:
                sentences = paragraph.replace(". ", ".\n").split("\n")
                temp_chunk = ""
                
                for sentence in sentences:
                    if count_tokens(temp_chunk + sentence) > max_tokens:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        
                        # If a single sentence is too long, just truncate it
                        if count_tokens(sentence) > max_tokens:
                            # Split the sentence into pieces
                            words = sentence.split()
                            temp = ""
                            for word in words:
                                if count_tokens(temp + word) > max_tokens:
                                    chunks.append(temp.strip())
                                    temp = word + " "
                                else:
                                    temp += word + " "
                            if temp:
                                chunks.append(temp.strip())
                        else:
                            chunks.append(sentence.strip())
                        temp_chunk = ""
                    else:
                        temp_chunk += sentence + " "
                
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
            else:
                current_chunk = paragraph + "\n\n"
        else:
            current_chunk += paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

async def generate_embeddings(text):
    """Generate embeddings for the given text using OpenAI's embeddings API."""
    try:
        # Check if text is too large for the model
        if count_tokens(text) > 8000:  # Using 8000 as a safe limit (below 8192)
            print(f"Text is too large ({count_tokens(text)} tokens). Splitting into smaller chunks.")
            chunks = split_text(text)
            print(f"Split into {len(chunks)} chunks.")
            
            # For now, we'll just use the first chunk that fits
            # A more sophisticated approach could generate embeddings for all chunks and average them
            if chunks:
                print(f"Using first chunk with {count_tokens(chunks[0])} tokens.")
                response = await client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=chunks[0],
                )
                return response.data[0].embedding
            else:
                raise ValueError("Failed to split text into manageable chunks")
        else:
            response = await client.embeddings.create(
                model="text-embedding-ada-002",
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
