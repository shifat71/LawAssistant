import os
import re
from typing import List
import PyPDF2
import docx

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

def chunk_text(text: str, max_chunk_size: int = 500) -> List[str]:
    """
    Split text into chunks of approximately max_chunk_size characters.
    Tries to split at paragraph or sentence boundaries.
    """
    # First, split by paragraphs
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If paragraph is too long, split by sentences
        if len(paragraph) > max_chunk_size:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chunk_size:
                    current_chunk += " " + sentence if current_chunk else sentence
                else:
                    if current_chunk:  # Avoid empty chunks
                        chunks.append(current_chunk)
                    current_chunk = sentence
        else:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
            else:
                if current_chunk:  # Avoid empty chunks
                    chunks.append(current_chunk)
                current_chunk = paragraph
    
    # Add the final chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
