import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Interpreter.Interpreter import Interpreter
from Logger.logger import log_error
import Token
import AST
import Errors


def run_repl():
    print("Loom REPL v0.1")
    print("Type 'exit' to quit.")
    print()

    interpreter = Interpreter(AST.Program([]))

    buffer = ""
    brace_depth = 0

    while True:

        try:
            prompt = (
                "Loom> "
                if not buffer
                else "...>" + "\t" * brace_depth
            )

            source = input(prompt)

        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if source.strip() == "exit":
            print("Bye!")
            break

        if source.strip() == "":
            continue

        # Automatically add semicolon to simple statements.
        if (
            not source.strip().endswith(";")
            and not source.strip().endswith("}")
        ):
            source = source.strip() + ";"

        buffer += source + "\n"

        try:
            tokens = Lexer(buffer)

            brace_depth = 0

            for token in tokens:
                if token.type == Token.TokenType.LBRACE:
                    brace_depth += 1

                elif token.type == Token.TokenType.RBRACE:
                    brace_depth -= 1

            if brace_depth > 0:
                continue

            parser = Parser(tokens)
            program = parser.parse_program()

            result = interpreter.execute(program)

            if result is not None:
                print(result)

            buffer = ""

        except Errors.LoomLexerError as e:
            log_error(e)
            print(f"Lexer error: {e}")
            buffer = ""
            brace_depth = 0

        except Errors.LoomParseError as e:
            log_error(e)
            print(f"Parse error: {e}")
            buffer = ""
            brace_depth = 0

        except Errors.LoomRuntimeError as e:
            log_error(e)
            print(f"Runtime error: {e}")
            buffer = ""
            brace_depth = 0


if __name__ == "__main__":
    run_repl()