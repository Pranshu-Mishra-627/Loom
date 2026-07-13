import Token
import lex_number
import lex_string
import lex_emotion_tag
import lex_name
import skip_comment

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