import numpy as np
import faiss

from embeddings.embedding_generator import generate_embedding
from parsers.skill_parser import extract_skills


def search_resumes(query, index, resume_data, top_k=5):

    # ---------------------------------------------------
    # 1. Extract required skills from the job description
    # ---------------------------------------------------

    required_skills = extract_skills(query)

    # ---------------------------------------------------
    # 2. Generate embedding for the query
    # ---------------------------------------------------

    query_embedding = generate_embedding(query).astype(np.float32)

    # FAISS expects shape: (number_of_queries, embedding_dimension)
    query_embedding = np.array([query_embedding])

    # Normalize for cosine similarity
    faiss.normalize_L2(query_embedding)

    # ---------------------------------------------------
    # 3. Retrieve more candidates from FAISS
    # ---------------------------------------------------

    candidate_count = min(20, len(resume_data))

    scores, indices = index.search(
        query_embedding,
        candidate_count
    )

    results = []

    # ---------------------------------------------------
    # 4. Calculate combined score
    # ---------------------------------------------------

    for semantic_score, idx in zip(scores[0], indices[0]):

        # Ignore invalid FAISS indices
        if idx < 0:
            continue

        resume = resume_data[idx]

        candidate_skills = set(resume["skills"])

        # Calculate skill match
        if required_skills:

            matched_skills = [
                skill
                for skill in required_skills
                if skill in candidate_skills
            ]

            skill_score = (
                len(matched_skills) / len(required_skills)
            )

        else:

            matched_skills = []
            skill_score = 0.0

        # Combined score
        overall_score = (
            0.7 * float(semantic_score)
            + 0.3 * skill_score
        )

        results.append({
            "filename": resume["filename"],
            "filepath": resume["filepath"],
            "email": resume["email"],
            "text": resume["text"],
            "skills": resume["skills"],

            "semantic_score": float(semantic_score),
            "skill_score": float(skill_score),
            "overall_score": float(overall_score),

            "required_skills": required_skills,
            "matched_skills": matched_skills
        })

    # ---------------------------------------------------
    # 5. Sort by overall score
    # ---------------------------------------------------

    results.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )

    # ---------------------------------------------------
    # 6. Return final top candidates
    # ---------------------------------------------------

    return results[:top_k]

