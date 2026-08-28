# from utils.file_loader import get_resume_files

# resume_files = get_resume_files("resumes")

# print(f"Total resumes found: {len(resume_files)}\n")

# for resume in resume_files:
#     print(resume.name)

# from extractors.pdf_extractor import extract_text_from_pdf

# file_path = "resumes/Priya_Validated.pdf"

# text = extract_text_from_pdf(file_path)

# print(text)

# from utils.file_loader import get_resume_files
# from extractors.pdf_extractor import extract_text_from_pdf
# from extractors.docx_extractor import extract_text_from_docx
# from parsers.email_parser import extract_email
# from embeddings.embedding_generator import generate_embedding
# from utils.data_manager import save_resume_data

# print("Program started...")

# resume_files = get_resume_files("resumes")

# resume_data = []

# for file in resume_files:

#     try:
#         print(f"processing: {file.name}")

#         if file.suffix.lower() == ".pdf":
#             text = extract_text_from_pdf(file)

#         elif file.suffix.lower() == ".docx":
#             text = extract_text_from_docx(file)

#         else:
#             continue

#         if not text.strip():
#             print(f"Skipping {file.name} (No text found)")
#             continue

#         print(f"Finished: {file.name}")

#         email = extract_email(text)

#         resume = {
#             "filename": file.name,
#             "email": email,
#             "text": text
#         }

#         print(f"Generating embedding for {file.name}...")

#         resume["embedding"] = generate_embedding(text)

#         resume_data.append(resume)

#         print(f"Finished: {file.name}")

#         save_resume_data(resume_data)

#     except Exception as e:
#         print(f"Error processing {file.name}: {e}")

# print("Resume database saved successfully!")    

# print(f"Loaded {len(resume_data)} resumes.\n")

# # Display first 3 resumes

# for resume in resume_data[:3]:

#     print("=" * 50)
#     print("Filename :", resume["filename"])
#     print("Email    :", resume["email"])
#     print("Text Preview:")
#     print(resume["text"][:300])
#     print()

from utils.file_loader import get_resume_files
from extractors.pdf_extractor import extract_text_from_pdf
from extractors.docx_extractor import extract_text_from_docx
from parsers.email_parser import extract_email
from embeddings.embedding_generator import generate_embedding
from utils.data_manager import save_resume_data
from parsers.skill_parser import extract_skills

print("Program started...\n")

# Load all resume files
resume_files = get_resume_files("resumes")

# List to store processed resume data
resume_data = []

for file in resume_files:

    try:
        print(f"Processing: {file.name}")

        # Extract text based on file type
        if file.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(file)

        elif file.suffix.lower() == ".docx":
            text = extract_text_from_docx(file)

        else:
            continue

        # Skip empty resumes
        if not text.strip():
            print(f"Skipping {file.name} (No text found)\n")
            continue

        print(f"Text extracted from: {file.name}")

        # Extract email
        email = extract_email(text)

        skills = extract_skills(text)

        # Create resume dictionary
        resume = {
            "filename": file.name,
            "filepath": str(file),
            "email": email,
            "text": text,
            "skills": skills
        }

        # Generate embedding
        print(f"Generating embedding for {file.name}...")
        resume["embedding"] = generate_embedding(text)

        # Store resume
        resume_data.append(resume)

        print(f"Finished: {file.name}\n")

    except Exception as e:
        print(f"Error processing {file.name}: {e}\n")

# Save all processed resumes
save_resume_data(resume_data)

print("Resume database saved successfully!")
print(f"Loaded {len(resume_data)} resumes.\n")

# Preview first 3 resumes
print("Showing first 3 resumes:\n")

for resume in resume_data[:3]:
    print("=" * 50)
    print("Filename :", resume["filename"])
    print("Email    :", resume["email"])
    print("Text Preview:")
    print(resume["text"][:300])
    print()

    