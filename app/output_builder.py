from datetime import datetime
import re
import numpy as np

def cosine_similarity(vec1, vec2):
    num = np.dot(vec1, vec2)
    denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return num / denom if denom > 0 else 0

def summarize_section_with_embeddings(text, model, query_embedding, top_n=5):
    # Split text into sentences (simple regex split on '.', '?', '!')
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    if len(sentences) <= top_n:
        return ' '.join(sentences)

    # Embed sentences
    sentence_embeddings = model.encode(sentences, convert_to_numpy=True, show_progress_bar=False)

    # Calculate cosine similarity with query
    scores = [cosine_similarity(s_emb, query_embedding) for s_emb in sentence_embeddings]

    # Get indices of top scoring sentences
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]

    # Sort sentences in original order for readability
    top_indices.sort()

    summary = ' '.join([sentences[i] for i in top_indices])
    return summary

def build_output_json(input_docs, persona, job, ranked_sections, model, query_embedding, top_n_sentences=5):
    output = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for sec in ranked_sections:
        output["extracted_sections"].append({
            "document": sec['document'],
            "section_title": sec.get('section_title', f"Page {sec.get('page', '?')}"),
            "importance_rank": sec['importance_rank'],
            "page_number": sec['page']
        })

        refined = summarize_section_with_embeddings(sec['text'], model, query_embedding, top_n=top_n_sentences)

        output["subsection_analysis"].append({
            "document": sec['document'],
            "refined_text": refined,
            "page_number": sec['page']
        })

    return output
