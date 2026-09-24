import Token
import Errors


def lex_tag(text: str, i: int):
    tag = ""
    i += 1

    while i < len(text) and text[i].isalpha():
        tag += text[i]
        i += 1

    if tag == "":
        raise Errors.LoomLexerError("Invalid tag statement")

    return i, Token.TokenType.TAG, tag