import requests
from bs4 import BeautifulSoup
import os
import re

def fetch_html(url):
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def clean_html_to_markdown(html_content):
    """Clean HTML and convert to markdown."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove specified sections
    for section in soup.select('section.bt-act-repealed'):
        section.decompose()
    
    for section in soup.select('section.copy-right'):
        section.decompose()
    
    # Remove all style, script tags
    for tag in soup.find_all(['style', 'script']):
        tag.decompose()
    
    # Remove all images
    for img in soup.find_all('img'):
        img.decompose()
    
    # Replace links with just their text
    for a in soup.find_all('a'):
        a.replace_with(a.get_text())
    
    # Extract the main content section
    main_content = soup.select_one('.col-md-11.hide-bod.boxed-layout')
    
    if not main_content:
        return "No content found"
    
    # Initialize markdown output
    markdown = []
    
    # Extract title
    title_section = main_content.select_one('section.bg-act-section')
    if title_section:
        title = title_section.select_one('h3')
        if title:
            markdown.append(f"# {title.text.strip()}\n")
    
    # Extract publication date
    publish_date = main_content.select_one('.publish-date')
    if publish_date:
        markdown.append(f"**{publish_date.text.strip()}**\n\n")
    
    # Extract act purpose/preamble
    act_role = main_content.select_one('.act-role-style')
    if act_role:
        markdown.append(f"**{act_role.text.strip()}**\n\n")
    
    preamble = main_content.select_one('.repealed .pad-right')
    if preamble:
        markdown.append(f"{preamble.text.strip()}\n\n")
    
    # Process each section with headings and content
    for row in main_content.select('.row.lineremoves'):
        # Extract heading
        heading_elem = row.select_one('.txt-head')
        if heading_elem:
            heading_text = heading_elem.text.strip()
            markdown.append(f"## {heading_text}\n")
        
        # Extract content
        content_elem = row.select_one('.txt-details')
        if content_elem:
            # Get text content preserving structure
            content_text = content_elem.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            content_text = re.sub(r'\s+', ' ', content_text).strip()
            markdown.append(f"{content_text}\n\n")
    
    # Join all markdown parts and clean up
    markdown_text = '\n'.join(markdown)
    
    # Clean excessive whitespace
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    return markdown_text

def save_markdown(content, filepath):
    """Save markdown content to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Saved: {filepath}")

def main():
    # Create data directory if it doesn't exist
    data_dir = "/Users/shaifurrahaman/Desktop/Projects/Datatify/LawAssistant/model/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Process pages 1 through 5
    for page_number in range(1, 6):
        url = f"http://bdlaws.minlaw.gov.bd/act-print-{page_number}.html"
        output_file = os.path.join(data_dir, f"law-{page_number}.md")
        
        print(f"Processing page {page_number}...")
        html_content = fetch_html(url)
        
        if html_content:
            markdown_content = clean_html_to_markdown(html_content)
            save_markdown(markdown_content, output_file)
        else:
            print(f"Failed to fetch page {page_number}")

if __name__ == "__main__":
    main()
