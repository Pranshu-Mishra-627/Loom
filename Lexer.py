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


def Lexer(text: str):
    Tokens = []
    i = 0

    while i < len(text):

        if text[i].isspace():
            i += 1

        elif text[i].isalpha() or text[i] == "_":
            i, token_type, asset = lex_name(text, i)
            Tokens.append(Token.TokenInfo(token_type, asset))

        elif text[i].isnumeric():
            i, token_type, asset = lex_number(text, i)
            Tokens.append(Token.TokenInfo(token_type, asset))

        elif text[i] == "\"":
            i, token_type, asset = lex_string(text, i)
            Tokens.append(Token.TokenInfo(token_type, asset))

        elif text[i] == "@":
            i, token_type, asset = lex_emotion_tag(text, i)
            Tokens.append(Token.TokenInfo(token_type, None, asset))

        elif text.startswith("==", i):
            Tokens.append(Token.TokenInfo(Token.TokenType.EQ, "=="))
            i += 2

        elif text.startswith("!=", i):
            Tokens.append(Token.TokenInfo(Token.TokenType.NE, "!="))
            i += 2

        elif text.startswith("<=", i):
            Tokens.append(Token.TokenInfo(Token.TokenType.LE, "<="))
            i += 2

        elif text.startswith(">=", i):
            Tokens.append(Token.TokenInfo(Token.TokenType.GE, ">="))
            i += 2

        elif text.startswith("//", i):
            i = skip_comment(text, i)

        elif text[i] == "=":
            Tokens.append(Token.TokenInfo(Token.TokenType.ASSIGN, "="))
            i += 1

        elif text[i] == "<":
            Tokens.append(Token.TokenInfo(Token.TokenType.LT, "<"))
            i += 1

        elif text[i] == ">":
            Tokens.append(Token.TokenInfo(Token.TokenType.GT, ">"))
            i += 1

        elif text[i] == "+":
            Tokens.append(Token.TokenInfo(Token.TokenType.PLUS, "+"))
            i += 1

        elif text[i] == "-":
            Tokens.append(Token.TokenInfo(Token.TokenType.MINUS, "-"))
            i += 1

        elif text[i] == "*":
            Tokens.append(Token.TokenInfo(Token.TokenType.STAR, "*"))
            i += 1

        elif text[i] == "/":
            Tokens.append(Token.TokenInfo(Token.TokenType.SLASH, "/"))
            i += 1

        elif text[i] == "%":
            Tokens.append(Token.TokenInfo(Token.TokenType.MOD, "%"))
            i += 1

        elif text[i] == ",":
            Tokens.append(Token.TokenInfo(Token.TokenType.COMMA, ","))
            i += 1

        elif text[i] == ";":
            Tokens.append(Token.TokenInfo(Token.TokenType.SEMICOLON, ";"))
            i += 1

        elif text[i] == "(":
            Tokens.append(Token.TokenInfo(Token.TokenType.LPAREN, "("))
            i += 1

        elif text[i] == ")":
            Tokens.append(Token.TokenInfo(Token.TokenType.RPAREN, ")"))
            i += 1

        elif text[i] == "{":
            Tokens.append(Token.TokenInfo(Token.TokenType.LBRACE, "{"))
            i += 1

        elif text[i] == "}":
            Tokens.append(Token.TokenInfo(Token.TokenType.RBRACE, "}"))
            i += 1

        else:
            raise ValueError(f"Unknown character '{text[i]}'")

    Tokens.append(Token.TokenInfo(Token.TokenType.EOF, "EOF"))
    return Tokens


def lex_name(text: str, i: int):
    identifier = ""

    while i < len(text) and (text[i].isalnum() or text[i] == "_"):
        identifier += text[i]
        i += 1

    keyword = get_keyword(identifier)

    if keyword is not None:
        return i, keyword, identifier

    return i, Token.TokenType.NAME, identifier


def lex_number(text: str, i: int):
    number = ""
    dot_count = 0

    while i < len(text):

        if text[i].isdigit():
            number += text[i]

        elif text[i] == ".":
            if dot_count == 1:
                break
            dot_count += 1
            number += "."

        else:
            break

        i += 1

    if number.endswith("."):
        raise ValueError("Invalid floating-point number")

    return i, Token.TokenType.NUMBER, number


def lex_string(text: str, i: int):
    string = ""
    i += 1

    while i < len(text):

        if text[i] == "\"":
            return i + 1, Token.TokenType.STRING, string

        string += text[i]
        i += 1

    raise ValueError("Unterminated string")


def lex_emotion_tag(text: str, i: int):
    tag = ""
    i += 1

    while i < len(text) and text[i].isalpha():
        tag += text[i]
        i += 1

    if tag == "":
        raise ValueError("Invalid emotion tag")

    return i, Token.TokenType.EMOTION_TAG, tag


def skip_comment(text: str, i: int):
    while i < len(text) and text[i] != "\n":
        i += 1

    return i


def get_keyword(identifier: str):
    return KEYWORD_MAP.get(identifier)