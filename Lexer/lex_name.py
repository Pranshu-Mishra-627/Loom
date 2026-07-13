import Token

KEYWORD_MAP = {
    "if": Token.TokenType.IF,
    "elif": Token.TokenType.ELIF,
    "else": Token.TokenType.ELSE,
    "while": Token.TokenType.WHILE,
    "def": Token.TokenType.DEF,
    "return": Token.TokenType.RETURN,
    "print": Token.TokenType.PRINT,
    "True": Token.TokenType.TRUE,
    "False": Token.TokenType.FALSE,
    "None": Token.TokenType.NONE,
    "and": Token.TokenType.AND,
    "or": Token.TokenType.OR,
    "not": Token.TokenType.NOT,
}

def lex_name(text: str, i: int):
    identifier = ""

    while i < len(text) and (text[i].isalnum() or text[i] == "_"):
        identifier += text[i]
        i += 1

    keyword = get_keyword(identifier)

    if keyword is not None:
        return i, keyword, identifier

    return i, Token.TokenType.NAME, identifier


def get_keyword(identifier: str):
    return KEYWORD_MAP.get(identifier)

