from sentence_transformers import SentenceTransformer

def load_model(model_name):
    return SentenceTransformer(model_name)

def embed_texts(model, texts):
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
