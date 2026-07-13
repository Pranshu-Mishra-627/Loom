import Token
def lex_string(text: str, i: int):
    string = ""
    i += 1

    while i < len(text):

        if text[i] == "\"":
            return i + 1, Token.TokenType.STRING, string

        string += text[i]
        i += 1

    raise ValueError("Unterminated string")