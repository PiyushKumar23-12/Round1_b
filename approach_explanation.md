

# 🧠 Persona-Driven Document Intelligence

*Challenge Theme: "Connect What Matters — For the User Who Matters"*

---

## 📘 Introduction

**Persona-Driven Document Intelligence** is a smart system that analyzes collections of PDFs to extract, rank, and summarize content relevant to a **specific user persona** and their **goal or task**. It’s designed to work across a wide variety of document types and roles — from research and business to travel and planning.


## ❓ Problem Statement

**Given:**

* A set of PDFs (3–10 documents)
* A user **persona** (e.g., "Travel Planner", "PhD Researcher")
* A **job-to-be-done** (e.g., "Plan a 4-day trip for a group of friends")

**The system must:**

1. Understand the persona and intent.
2. Extract relevant document sections.
3. Rank them based on importance.
4. Summarize them into concise, focused insights.

---

## ⚙️ How It Works

1. **Input Parsing**

   * Reads `input.json` for persona and task details.
2. **PDF Section Extraction**

   * Loads each PDF with `PyMuPDF`, page by page.
   * Extracts text and likely section titles.
3. **Semantic Embedding**

   * Converts persona+task and document sections into vectors using `Sentence-BERT (MiniLM)`.
4. **Section Ranking**

   * Computes cosine similarity to rank document sections by relevance.
5. **Summarization**

   * Selects top-N sentences from top-ranked sections.
6. **Structured Output**

   * Writes insights and rankings into `output.json`.

---

## 📁 Directory Structure

```plaintext
persona-doc-intelligence/
├── app/
│   ├── config.py               # Configuration constants
│   ├── main.py                 # Main execution logic
│   ├── pdf_processor.py        # Extracts text and titles from PDFs
│   ├── embedding_utils.py      # Loads transformer model and generates embeddings
│   ├── ranking.py              # Ranks document sections using cosine similarity
│   └── output_builder.py       # Builds refined summaries and final JSON output
├── collection/
│   ├── input.json              # Persona and task input
│   ├── output.json             # Final generated output
│   └── pdfs/                   # Input PDF documents
│       ├── South of France - Cities.pdf
│       └── ...
├── requirements.txt            # Required Python packages
└── Dockerfile                  # For containerized execution
```

---

## 💻 Installation

### Option 1: Docker (Recommended)

```bash
# Build the Docker image
docker build -t doc-intelligence .

# Run the container with mounted volume
docker run --rm -v $(pwd)/collection:/app/collection doc-intelligence
```

### Option 2: Manual Python Setup

```bash
# Clone the repo
git clone https://github.com/your-repo/persona-doc-intelligence.git
cd persona-doc-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📥 Input Format

### `collection/input.json`

```json
{
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  },
  "document_metadata": [
    {
      "filename": "South of France - Cities.pdf",
      "description": "Guide covering key cities in Southern France including Nice, Marseille, and Avignon."
    },
    {
      "filename": "French Cuisine Highlights.pdf",
      "description": "Details about must-try foods and local specialties in different French regions."
    }
  ]
}
```

📌 Make sure all referenced files are in `collection/pdfs/`.

---

## 📤 Output Format

### `collection/output.json`

```json
{
  "metadata": {
    "persona_role": "Travel Planner",
    "task": "Plan a trip of 4 days for a group of 10 college friends",
    "processed_on": "2025-07-28",
    "documents_count": 2
  },
  "extracted_sections": [
    {
      "document": "South of France - Cities.pdf",
      "section_title": "Nice & Marseille",
      "importance_rank": 1,
      "page_number": 3
    },
    {
      "document": "French Cuisine Highlights.pdf",
      "section_title": "Street Foods in Provence",
      "importance_rank": 2,
      "page_number": 5
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cities.pdf",
      "refined_text": "Nice offers beachside charm and group-friendly nightlife. Marseille provides cultural experiences ideal for day trips.",
      "page_number": 3
    },
    {
      "document": "French Cuisine Highlights.pdf",
      "refined_text": "Must-try foods include Socca in Nice and Bouillabaisse in Marseille—great for shared meals.",
      "page_number": 5
    }
  ]
}
```

---

## 🧰 Technologies Used

| Component      | Technology                          |
| -------------- | ----------------------------------- |
| PDF Processing | PyMuPDF                             |
| Embeddings     | SentenceTransformers (MiniLM)       |
| Ranking Logic  | Cosine Similarity (NumPy)           |
| Summarization  | Sentence-level embedding comparison |
| Deployment     | Docker (Multi-stage build)          |

---

## 💡 Example Use Cases

* 👨‍🎓 A **PhD student** filtering 50 research papers by a research question.
* 🧳 A **travel agent** planning a customized itinerary from regional guides.
* 🧑‍💼 A **market analyst** scanning industry reports for business strategy insights.
