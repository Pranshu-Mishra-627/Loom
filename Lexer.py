def Lexer(text: str):

    i = 0
    while i < len(text):
        if text[i].isspace():
            i+=1
            continue
        elif text[i].isalpha():
            i += print_identifier(text, i)
        elif text[i].isnumeric():
            i += print_number(text, i)            
        elif text[i] == "=":
            print(f"Assign({text[i]})")
            i+=1
        elif text[i] == "+":
            print(f"Add({text[i]})")
            i+=1
        elif text[i]== "(":
            print("OpenBrace")
            i+=1
        elif text[i]== ")":
            print("CloseBrace")
            i+=1
        elif text[i]== "*":
            print("Multiply")
        else: 
            print(f"UNDEFINED ({text[i]})")
            i+=1
        

def print_identifier(text: str, i: int):
    iden = ""
    for j in range(i, len(text)):
        if(text[j].isalnum() or text[j] == "_"):
            iden += text[j]
        else: break
    print(f"Identifier({iden})")
    return len(iden)

def print_number(text: str, i: int):
    number = ""
    for j in range(i, len(text)):
        if(text[j].isnumeric()):
            number+= text[j]
        else: break
    print(f"Number({number})")
    return len(number)