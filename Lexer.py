def Lexer(text: str):
    i = 0
    while i < len(text):
        if text[i].isspace():
            i+=1
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
            i+=1
        elif text[i]== ";":
            print("End of Statement (;)")
            i+=1
        elif text.startswith("//", i):
            i += skip_comment(text, i)
        elif text[i]== "/":
            print("Divide")
            i+=1
        else: 
            print(f"UNDEFINED ({text[i]})")
            i+=1
    
    print("EOF")

def print_identifier(text: str, i: int):
    iden = ""
    for j in range(i, len(text)):
        if(text[j].isalnum() or text[j] == "_"):
            iden += text[j]
        else: break
    
    keyword = is_keyword(iden)

    if keyword:
        print(f"Keyword({iden})")
    else:
        print(f"Identifier({iden})")
    return len(iden)

def skip_comment(text:str, i:int):
    count = 0
    for j in range(i, len(text)):
        if(text[j] == "\n"): 
            break
        count +=1
    return count

def print_number(text: str, i: int):
    number = ""
    for j in range(i, len(text)):
        if(text[j].isnumeric()):
            number+= text[j]
        else: break
    print(f"Number({number})")
    return len(number)


#--------------helpers---------------------#
def is_keyword(identifier: str):
    keywords = {
    "if",
    "elif",
    "else",
    "while",
    "def",
    "return",
    "print",
    "True",
    "False",
    "None",
    "and",
    "or",
    "not"
    }

    return identifier in keywords
