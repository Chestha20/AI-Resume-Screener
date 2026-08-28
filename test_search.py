from utils.data_manager import load_resume_data
from faiss_index.index_builder import build_faiss_index
from search.search_engine import search_resumes

resume_data = load_resume_data()

index = build_faiss_index(resume_data)

query = input("Enter Job Description: ")

results = search_resumes(
    query,
    index,
    resume_data
)

print("\nTop Matching Resumes\n")

for i, resume in enumerate(results, start=1):

    print("=" * 40)

    print(f"Rank : {i}")

    print(f"Filename : {resume['filename']}")

    print(f"Email : {resume['email']}")

    print(f"Cosine Similarity : {resume['score']:.4f}")
