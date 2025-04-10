import os
import re
from typing import List, Dict, Any

async def read_law_files(directory: str = None) -> List[Dict[str, str]]:
    """Read all law files from the specified directory."""
    if directory is None:
        # Use relative path from this file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory = os.path.join(current_dir, 'model', 'data')
    
    law_texts = []

    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist")
        return law_texts

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    law_texts.append({
                        "fileName": file,
                        "filePath": file_path,
                        "content": content
                    })
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return law_texts

def split_into_chunks(law_texts: List[Dict[str, str]], max_chunk_size: int = 1000) -> List[Dict[str, str]]:
    """Split law documents into smaller chunks."""
    chunks = []

    for law in law_texts:
        content = law["content"]
        
        # Split content into paragraphs
        paragraphs = re.split(r'\n\s*\n', content)
        current_chunk = ''
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) > max_chunk_size and current_chunk:
                chunks.append({
                    "fileName": law["fileName"],
                    "filePath": law["filePath"],
                    "content": current_chunk.strip()
                })
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += '\n\n' + paragraph
                else:
                    current_chunk = paragraph
        
        if current_chunk.strip():
            chunks.append({
                "fileName": law["fileName"],
                "filePath": law["filePath"],
                "content": current_chunk.strip()
            })
    
    return chunks
