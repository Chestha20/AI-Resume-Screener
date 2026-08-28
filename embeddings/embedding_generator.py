from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully!")


def generate_embedding(text):
    return model.encode(text, convert_to_numpy=True)