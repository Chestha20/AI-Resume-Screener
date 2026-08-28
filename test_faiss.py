from utils.data_manager import load_resume_data
from faiss_index.index_builder import build_faiss_index

resume_data = load_resume_data()

index = build_faiss_index(resume_data)

print(index.ntotal)
