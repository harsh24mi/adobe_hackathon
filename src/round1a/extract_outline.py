# src/round1a/extract_outline.py
import fitz  # PyMuPDF
import json
import os
from collections import Counter

def analyze_fonts(doc):
    """Analyzes font sizes and styles to guess body text and heading levels."""
    font_counts = Counter()
    # Iterate through pages and text blocks to count font styles
    for page in doc:
        blocks = page.get_text("dict").get("blocks", [])
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Store font size and flags (bold, italic, etc.)
                        font_counts[(span["size"], span["flags"])] += 1
    
    if not font_counts:
        return None, {}
    
    # Assume the most common font style is body text
    body_font = font_counts.most_common(1)[0][0]
    
    # Identify potential heading fonts (larger than body text)
    heading_fonts = sorted(
        [font for font, count in font_counts.items() if font[0] > body_font[0]], 
        key=lambda x: x[0], 
        reverse=True
    )
    
    # Map the largest fonts to H1, H2, H3
    level_map = {}
    if len(heading_fonts) > 0: level_map[heading_fonts[0]] = "H1"
    if len(heading_fonts) > 1: level_map[heading_fonts[1]] = "H2"
    if len(heading_fonts) > 2: level_map[heading_fonts[2]] = "H3"
    
    return body_font, level_map

def extract_structure(pdf_path):
    """Extracts title and a structured outline from a PDF."""
    doc = fitz.open(pdf_path)
    
    # --- NEW TITLE LOGIC ---
    title = "Untitled"
    max_font_size = 0
    # Only check the first page for the title
    first_page = doc[0] 

    for block in first_page.get_text("dict")["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["size"] > max_font_size:
                        max_font_size = span["size"]
                        # Clean up the text
                        title = span["text"].strip()
    # --- END NEW TITLE LOGIC ---

    body_font, level_map = analyze_fonts(doc)
    outline = []

    if not level_map:
        # Still return the title even if no outline is found
        return {"title": title, "outline": outline}

    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict").get("blocks", [])
        for block in blocks:
            if "lines" in block:
                line = block["lines"][0]
                span = line["spans"][0]
                font_style = (span["size"], span["flags"])
                
                if font_style in level_map:
                    text = "".join([s["text"] for s in line["spans"]]).strip()
                    # Avoid adding the document title to the outline
                    if text.lower() != title.lower():
                        outline.append({
                            "level": level_map[font_style],
                            "text": text,
                            "page": page_num
                        })
                            
    return {"title": title, "outline": outline}

def process_all_pdfs(input_dir, output_dir):
    """
    Processes all PDFs from the input directory and saves a corresponding
    JSON file to the output directory, as required by the challenge.
    """
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            try:
                result = extract_structure(pdf_path)
                
                # The output must be filename.json for each filename.pdf
                output_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(output_dir, output_filename)
                
                # The output must be a valid JSON file [cite: 21]
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                print(f"Processed {filename} -> {output_filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    # This reflects the Docker execution environment specified in the rules 
    # where the script processes files from /app/input to /app/output.
    input_directory = "/app/input"
    output_directory = "/app/output"
    
    # For local testing, you can change these paths.
    # For example, use 'input' and 'output' for the folders in your project root.
    if not os.path.exists(input_directory):
        print("Running in local mode. Using local 'input' and 'output' directories.")
        input_directory = "input"
        output_directory = "output"

    process_all_pdfs(input_directory, output_directory)