import Token
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
    
    if "." in number:
        return i, Token.TokenType.NUMBER, float(number)
    
    return i, Token.TokenType.NUMBER, int(number)
