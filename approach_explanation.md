# Persona-Driven Document Intelligence

*Challenge Theme: "Connect What Matters — For the User Who Matters"*

## Overview

This system serves as an intelligent document analyst that reads a set of PDFs and extracts, ranks, and summarizes the most relevant sections based on:

- A defined persona (user role)
- Their job-to-be-done (task)

It's built to generalize across diverse document types, user roles, and tasks — from research literature reviews to business analysis and travel planning.

## Problem Statement

*Given:*
- A collection of PDFs (3-10 documents)
- A persona description (e.g., "Travel Planner", "PhD Researcher")
- A task the persona wants to accomplish

*The system must:*
- Understand the persona and their intent
- Extract meaningful sections from PDFs
- Rank them by relevance
- Summarize them into concise, task-focused insights

## Directory Structure


project/
├── app/
│   ├── config.py                Configuration constants
│   ├── main.py                  Main execution logic
│   ├── pdf_processor.py        # Extracts text and titles from PDFs
│   ├── embedding_utils.py      # Loads transformer model and generates embeddings
│   ├── ranking.py              # Ranks document sections using cosine similarity
│   └── output_builder.py       # Builds refined summaries and final JSON output
├── collection/
│   ├── input.json              # Persona and task input
│   ├── output.json             # Final generated output
│   └── pdfs/                   # Folder containing all input PDFs
│       ├── ...                 # e.g., South of France - Cities.pdf
├── requirements.txt            # Required Python packages
└── Dockerfile                  # For containerized execution


## How It Works

### 1. Input Parsing
The input.json file contains:
- Document metadata
- Persona (role)
- Job-to-be-done (task)

### 2. PDF Section Extraction
pdf_processor.py loads each PDF page-by-page using PyMuPDF.

*Extracts:*
- Clean text from each page
- Probable section titles (via font-size + position heuristics)

### 3. Semantic Embedding
Loads a Sentence-BERT model (all-MiniLM-L6-v2) via sentence-transformers.

*Encodes:*
- Each page/section's text → vector
- Combined persona+task → query vector

### 4. Section Ranking
Uses cosine similarity between each section and the query vector.

Assigns a rank (1 = most relevant) to each section (ranking.py).

### 5. Focused Summarization
output_builder.py splits the top sections into sentences.

Selects the top-N most relevant sentences (by cosine similarity) to form a refined summary for each section.

### 6. Structured Output
Outputs a collection/output.json file containing:
- Metadata
- Ranked section list
- Refined summaries (with page numbers and document names)

## Sample Input

json
"persona": {
  "role": "Travel Planner"
},
"job_to_be_done": {
  "task": "Plan a trip of 4 days for a group of 10 college friends."
}


## Technologies Used

| Component | Technology |
|-----------|------------|
| PDF Processing | PyMuPDF |
| Embeddings | SentenceTransformers (MiniLM) |
| Ranking | Cosine Similarity (NumPy) |
| Summarization | Sentence-level embedding comparison |
| Deployment | Docker (multi-stage) |

## Run with Docker

bash
# Build the image
docker build -t doc-intelligence .

# Run the container
docker run --rm -v $(pwd)/collection:/app/collection doc-intelligence


*Ensure your collection folder contains:*
- All PDFs under collection/pdfs/
- A properly formatted input.json

## Output Format

The output.json contains:

json
{
  "metadata": { ... },
  "extracted_sections": [
    {
      "document": "South of France - Cities.pdf",
      "section_title": "Nice & Marseille",
      "importance_rank": 1,
      "page_number": 3
    },
    ...
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cities.pdf",
      "refined_text": "Nice is known for its ...",
      "page_number": 3
    },
    ...
  ]
}
