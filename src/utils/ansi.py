import re

ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def clean_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text)
