from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Interpreter.Interpreter import Interpreter
import AST


with open("Parser/block_tag.loom", "r") as f:
    source = f.read()

tokens = Lexer(source)

parser = Parser(tokens)
program = parser.parse_program()

print("AST generated successfully!")
print()

for i, statement in enumerate(program.statements, 1):

    print(f"Statement {i}")
    print("Node type :", type(statement).__name__)

    if isinstance(statement, AST.AnnotationStatement):
        print("Tag name  :", statement.tag_name)
        print("Tag body  :", statement.tag_bodystr)
        print("Body type :", type(statement.body).__name__)

    print()


print("=" * 50)
print("INTERPRETER TEST")
print("=" * 50)

interpreter = Interpreter(program)
interpreter.execute(program)