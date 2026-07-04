import Lexer as Lex
with open("test/test1.loom", "r") as file:
    source = file.read()

tokens = Lex.Lexer(source)

for token in tokens:
    print(token)

