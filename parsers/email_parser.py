import re


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    matches = re.findall(pattern, text)

    if matches:
        return matches[0]

    return None