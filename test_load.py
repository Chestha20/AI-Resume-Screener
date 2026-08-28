from utils.data_manager import load_resume_data

resume_data = load_resume_data()

print(f"Total resumes: {len(resume_data)}")

print(resume_data[0].keys())

print(resume_data[0]["filename"])

print(resume_data[0]["email"])

print(resume_data[0]["embedding"].shape)