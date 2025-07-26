from pdf_processor import extract_sections_from_folder
from embedding_utils import load_model, embed_texts
from ranking import rank_sections
from output_builder import build_output_json
from config import MODEL_NAME, OUTPUT_FILE
import json
import sys

def main(pdf_folder, persona, job):
    print("Extracting sections from PDFs...")
    sections = extract_sections_from_folder(pdf_folder)
    if not sections:
        print("No sections found! Check your PDF folder.")
        return
    print(f"Extracted {len(sections)} sections")

    print("Loading embedding model...")
    model = load_model(MODEL_NAME)

    print("Embedding section texts...")
    texts = [sec['text'] for sec in sections]
    section_embeddings = embed_texts(model, texts)

    query = persona + " " + job
    print(f"Embedding query: '{query}' ...")
    query_embedding = embed_texts(model, [query])[0]

    print("Ranking sections...")
    ranked_sections = rank_sections(sections, section_embeddings, query_embedding)

    print("Building output JSON with top sentences as refined summaries...")
    input_docs = list({sec['document'] for sec in sections})
    output_json = build_output_json(
        input_docs, persona, job, ranked_sections, model, query_embedding, top_n_sentences=5
    )

    print("Saving output...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2)
    print(f"Output saved to {OUTPUT_FILE}")


def load_input_json(file_path="input.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]
    return persona, job

if __name__ == "__main__":
    # Assume PDFs are in 'pdfs/' folder in project root
    pdf_folder = "collection/pdfs"
    try:
        persona, job = load_input_json("collection/input.json")
    except Exception as e:
        print(f"Failed to load input.json: {e}")
        sys.exit(1)
    main(pdf_folder, persona, job)
