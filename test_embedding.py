from embeddings.embedding_generator import generate_embedding

text = "Python Developer with Machine Learning"

embedding = generate_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])
