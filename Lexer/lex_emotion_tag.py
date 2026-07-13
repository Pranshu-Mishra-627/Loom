import Token
def lex_emotion_tag(text: str, i: int):
    tag = ""
    i += 1

    while i < len(text) and text[i].isalpha():
        tag += text[i]
        i += 1

    if tag == "":
        raise ValueError("Invalid emotion tag")

    return i, Token.TokenType.EMOTION_TAG, tag