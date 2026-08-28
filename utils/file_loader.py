from pathlib import Path

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

def get_resume_files(folder_path):
    folder = Path(folder_path)

    resume_files = []

    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            resume_files.append(file)

    return resume_files
