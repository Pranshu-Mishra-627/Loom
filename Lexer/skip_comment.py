import Token
def skip_comment(text: str, i: int):
    while i < len(text) and text[i] != "\n":
        i += 1

    return i