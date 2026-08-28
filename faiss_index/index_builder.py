import faiss
import numpy as np


def build_faiss_index(resume_data):

    embeddings = np.array(
        [resume["embedding"] for resume in resume_data],
        dtype=np.float32
    )

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Inner Product Index
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index