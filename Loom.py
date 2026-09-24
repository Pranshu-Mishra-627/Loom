from Lexer import Lexer as Lex
from Parser import Parser
from Interpreter import Interpreter
import Errors
with open("test/stress_test.loom", "r") as file:
    source = file.read()

tokens = Lex.Lexer(source)
parser = Parser(tokens)
interpreter = Interpreter.Interpreter(parser)


