from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load model once (outside the function if possible)
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.save("./")
except Exception as load_err:
    model = None
    print(f"[ERROR] Could not load model: {load_err}")

def generate_embeddings(texts):
    embeddings = []
    
    if not model:
        raise RuntimeError("Embedding model not loaded. Cannot generate embeddings.")
    
    for text in texts:
        try:
            embedding = model.encode(text)
            embeddings.append(embedding.tolist())
        except Exception as e:
            # Fallback: Use a dummy embedding or skip
            print(f"[WARNING] Failed to encode '{text}': {e}")
            fallback_vector = np.zeros(384).tolist()  # 384 is the dim for all-MiniLM-L6-v2
            embeddings.append(fallback_vector)
    
    return embeddings
