# src/round1b/analyze_docs.py
import json
import os
import fitz
import torch
import time
from sentence_transformers import SentenceTransformer, util

def extract_sections_from_pdf(pdf_path, doc_name):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        if text.strip():
            sections.append({
                "doc_name": doc_name,
                "page": page_num,
                "text": text,
                "title": f"Content from Page {page_num}"
            })
    return sections

def analyze_collection(input_dir, output_dir):
    start_time = time.time()
    
    model_path = "/app/models/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_path)

    job_spec_path = os.path.join(input_dir, "job.json")
    if not os.path.exists(job_spec_path):
        print(f"Error: job.json not found in {input_dir}")
        return

    with open(job_spec_path, 'r', encoding='utf-8') as f:
        job_spec = json.load(f)
    
    persona = job_spec["persona"]["description"]
    job_to_be_done = job_spec["job_to_be_done"]["task"]
    query = f"Persona: {persona}. Task to be done: {job_to_be_done}"
    
    doc_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    all_sections = []
    for doc_file in doc_files:
        pdf_path = os.path.join(input_dir, doc_file)
        all_sections.extend(extract_sections_from_pdf(pdf_path, doc_file))

    if not all_sections:
        print("No sections found in any PDF.")
        return

    query_embedding = model.encode(query, convert_to_tensor=True)
    section_texts = [section['text'] for section in all_sections]
    section_embeddings = model.encode(section_texts, convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_embedding, section_embeddings)[0]
    for i, score in enumerate(cosine_scores):
        all_sections[i]['relevance_score'] = score.item()

    ranked_sections = sorted(all_sections, key=lambda x: x['relevance_score'], reverse=True)

    output_data = {
        "metadata": {
            "input_documents": doc_files,
            "persona": job_spec["persona"]["role"],
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        },
        "extracted_section": [
            {
                "document": s['doc_name'],
                "page_number": s['page'],
                "section_title": s['title'],
                "importance_rank": rank + 1
            } for rank, s in enumerate(ranked_sections)
        ],
        "sub_section_analysis": [] 
    }

    output_path = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    
    print(f"Analysis complete in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    analyze_collection("/app/input", "/app/output")