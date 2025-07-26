import numpy as np

def cosine_similarity(vec1, vec2):
    num = np.dot(vec1, vec2)
    denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return num / denom if denom > 0 else 0

def rank_sections(sections, section_embeddings, query_embedding):
    scores = [cosine_similarity(ev, query_embedding) for ev in section_embeddings]
    # Assign importance_rank: 1 = most relevant
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    ranked_sections = []
    for rank, idx in enumerate(ranked_indices, start=1):
        sec = sections[idx].copy()
        sec['importance_rank'] = rank
        ranked_sections.append(sec)
    return ranked_sections
