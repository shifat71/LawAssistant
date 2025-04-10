import os
import re
from typing import List
import PyPDF2
import docx
import tiktoken  # Add tiktoken import

async def process_document(file_path: str) -> str:
    """Extract text from a document based on its file extension."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fall back to cl100k_base encoding if model not found
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def chunk_text(text: str, max_tokens: int = 1000, model: str = "gpt-3.5-turbo") -> List[str]:
    """
    Split text into chunks based on token count rather than character count.
    Tries to split at paragraph or sentence boundaries.
    
    Args:
        text: The text to split into chunks
        max_tokens: Maximum number of tokens per chunk
        model: The OpenAI model to use for token counting
    
    Returns:
        List of text chunks
    """
    # First, split by paragraphs
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    current_token_count = 0
    
    # Try to get encoding for the specified model
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    for paragraph in paragraphs:
        paragraph_tokens = len(encoding.encode(paragraph))
        
        # If paragraph is too long, split by sentences
        if paragraph_tokens > max_tokens:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            for sentence in sentences:
                sentence_tokens = len(encoding.encode(sentence))
                
                if current_token_count + sentence_tokens <= max_tokens:
                    if current_chunk:
                        current_chunk += " " + sentence
                    else:
                        current_chunk = sentence
                    current_token_count += sentence_tokens
                else:
                    if current_chunk:  # Avoid empty chunks
                        chunks.append(current_chunk)
                    current_chunk = sentence
                    current_token_count = sentence_tokens
        else:
            if current_token_count + paragraph_tokens <= max_tokens:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                current_token_count += paragraph_tokens
            else:
                if current_chunk:  # Avoid empty chunks
                    chunks.append(current_chunk)
                current_chunk = paragraph
                current_token_count = paragraph_tokens
    
    # Add the final chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
