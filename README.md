# Adobe Hackathon: Connecting the Dots

This project is a solution for Round 1 of the Adobe "Connecting the Dots" Hackathon. It includes two main components: a document outline extractor (Round 1A) and a persona-driven document intelligence system (Round 1B).

## Features

* **Round 1A: Document Outline Extractor**
    * Accepts any PDF file.
    * Extracts the document's title and a hierarchical outline of headings (H1, H2, H3) with page numbers.
    * Handles simple, complex, and multilingual (e.g., Japanese, French) documents.
    * Outputs a structured JSON file for each processed PDF.

* **Round 1B: Persona-Driven Document Intelligence**
    * Analyzes a collection of multiple PDFs based on a specific user persona and a "job-to-be-done".
    * Uses a sentence-transformer AI model to understand the semantic context.
    * Ranks every section (page) from all documents by relevance to the user's task.
    * Outputs a single JSON file containing the ranked list of the most relevant sections.

## Approach

* **Round 1A**: A heuristic-based approach using the `PyMuPDF` library. It analyzes font properties (size, weight) to distinguish headings from body text. The title is identified as the text with the largest font on the first page.

* **Round 1B**: A semantic search approach. The user's query (persona + job) and all document sections are converted into vector embeddings using the `all-MiniLM-L6-v2` model. The relevance is calculated using cosine similarity between the query vector and each section vector.

## Models & Libraries

* **Models**: `all-MiniLM-L6-v2` (from `sentence-transformers`)
* **Libraries**: `PyMuPDF`, `sentence-transformers`, `torch` (CPU-only)

## How to Build and Run

### Round 1A
```bash
# Build the image
docker build --platform linux/amd64 -t round1a-solution -f src/round1a/Dockerfile .

# Run the container (place PDFs in the 'input' folder)
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none round1a-solution