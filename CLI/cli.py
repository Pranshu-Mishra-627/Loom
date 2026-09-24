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
import Errors


VERSION = "1.0.1"


def run_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        tokens = Lexer(source)
        parser = Parser(tokens)
        program = parser.parse_program()

        interpreter = Interpreter(program)
        interpreter.execute(program)

    except Errors.LoomLexerError as e:
        log_error(e, path)
        print(f"Lexer error: {e}")
        return 1

    except Errors.LoomParseError as e:
        log_error(e, path)
        print(f"Parse error: {e}")
        return 1

    except Errors.LoomRuntimeError as e:
        log_error(e, path)
        print(f"Runtime error: {e}")
        return 1

    except FileNotFoundError as e:
        error = FileNotFoundError(
            f"File not found: {path}"
        )
        log_error(error, path)
        print(f"Error: File not found: {path}")
        return 1

    except OSError as e:
        log_error(e, path)
        print(f"Error: Could not read file: {e}")
        return 1

    return 0


def print_help():
    print("Loom Programming Language")
    print()
    print("Usage:")
    print("  loom                  Start the Loom REPL")
    print("  loom <file.loom>     Run a Loom source file")
    print("  loom --help           Show this help message")
    print("  loom --version        Show Loom version")


def print_version():
    print(f"Loom {VERSION}")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        from REPL.repl import run_repl
        run_repl()
        return 0

    if args[0] in ("--help", "-h"):
        print_help()
        return 0

    if args[0] in ("--version", "-v"):
        print_version()
        return 0

    if args[0].startswith("-"):
        print(f"Unknown option: {args[0]}")
        print("Use 'loom --help' for usage information.")
        return 1

    if len(args) > 1:
        print("Error: Too many arguments.")
        print("Use 'loom --help' for usage information.")
        return 1

    return run_file(args[0])


if __name__ == "__main__":
    sys.exit(main())