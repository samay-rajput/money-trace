import re

def clean_text(text: str) -> str:
    # normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # remove leading/trailing spaces from each line
    lines = [line.strip() for line in text.split("\n")]

    # remove empty lines
    lines = [line for line in lines if line]

    # collapse multiple spaces
    lines = [re.sub(r"\s+", " ", line) for line in lines]

    return "\n".join(lines)