import pickle


def save_resume_data(resume_data, filename="data/resume_data.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(resume_data, file)


def load_resume_data(filename="data/resume_data.pkl"):
    with open(filename, "rb") as file:
        return pickle.load(file)