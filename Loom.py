import Lexer as Lex
with open("test/test1.loom", "r") as file:
    source = file.read()

print(source)
Lex.Lexer(source)
