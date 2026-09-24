# Loom

Loom is a small interpreted programming language built in Python as a
complete language implementation project.

It follows a classic interpreter pipeline:

``` text
Loom Source Code
       |
       v
     Lexer
       |
       v
    Parser
       |
       v
      AST
       |
       v
   Interpreter
       |
       v
    Program Output
```

Loom uses a C-like syntax and supports variables, expressions, control
flow, functions, recursion, annotations, a REPL, command-line execution,
and persistent error logging.

## Features

### Core language

-   Variables and assignment
-   Arithmetic operators
-   Comparison operators
-   Logical operators
-   Unary operators
-   Strings
-   Booleans
-   `none`
-   `if`, `elif`, and `else`
-   `while` loops
-   Functions
-   Function parameters
-   Return statements
-   Nested functions
-   Recursion
-   Function calls
-   Comments
-   `print()`

### Annotation system

Loom includes an annotation system using `@tag` syntax.

Example:

``` loom
@debug
x = 10;
```

Annotations are represented in the AST as metadata and can be displayed
when runtime tagging is enabled.

The language also provides the `tag()` built-in statement:

``` loom
tag();

@debug
x = 10;
```

`tag()` toggles annotation output at runtime.

### Error handling

Loom has a dedicated error hierarchy:

-   `LoomLexerError`
-   `LoomParseError`
-   `LoomRuntimeError`

Errors are reported to the user with clear error categories.

Loom also maintains a persistent local error log on Windows at:

``` text
%LOCALAPPDATA%\Loom\loom.log
```

The log records lexer, parser, runtime, and system/file errors with
timestamps.

### REPL

Loom includes an interactive REPL:

``` text
Loom> x = 10
Loom> print(x)
10
```

The REPL supports:

-   Multiline blocks
-   Nested blocks
-   Automatic semicolon insertion
-   Persistent interpreter state during the session
-   `exit` to leave the REPL

### Command-line interface

Loom can be used directly from the command line.

``` text
loom
loom program.loom
loom --help
loom --version
```

## Example Loom Program

``` loom
x = 10 + 20 * 3;

if (x > 50) {
    print("large");
} else {
    print("small");
}
```

Output:

``` text
large
```

A function example:

``` loom
def factorial(n) {
    if (n <= 1) {
        return 1;
    }

    return n * factorial(n - 1);
}

print(factorial(5));
```

Output:

``` text
120
```

## Project Structure

``` text
Loom/
|
├── AST.py
├── Token.py
├── Errors.py
|
├── Lexer/
|   ├── __init__.py
|   ├── Lexer.py
|   ├── lex_name.py
|   ├── lex_number.py
|   ├── lex_string.py
|   ├── lex_tag.py
|   └── skip_comment.py
|
├── Parser/
|   ├── __init__.py
|   ├── Parser.py
|   └── test_parser.py
|
├── Interpreter/
|   ├── __init__.py
|   ├── Interpreter.py
|   └── test_interpreter.py
|
├── REPL/
|   └── repl.py
|
├── CLI/
|   └── cli.py
|
├── Logger/
|   ├── __init__.py
|   └── logger.py
|
├── bin/
|   └── loom.bat
|
├── test/
|
└── releases/
    └── Loom.exe
```

## How Loom Works

### 1. Lexing

The lexer reads the source code and converts it into a sequence of
tokens.

For example:

``` loom
x = 10 + 20;
```

is broken into tokens representing:

``` text
identifier
assignment
number
plus
number
semicolon
```

The lexer is also responsible for recognizing strings, names, numbers,
comments, and annotation tags.

### 2. Parsing

The parser consumes the token stream and builds an Abstract Syntax Tree
(AST).

The AST represents the structure and meaning of the program rather than
its original text.

For example:

``` loom
x = 10 + 20;
```

becomes an assignment node containing an expression tree.

### 3. Interpretation

The tree-walking interpreter executes the AST directly.

It manages:

-   Variables
-   Environments and scopes
-   Functions
-   Function calls
-   Return flow
-   Control flow
-   Expressions
-   Runtime errors
-   Annotation output

Functions capture their surrounding environment, allowing nested
functions and recursion to work correctly.

## Running Loom

### Option 1: Standalone executable

A standalone Windows executable is included in the release.

``` text
Loom.exe
```

No Python installation or Loom source files are required to run the
standalone executable.

Start the REPL:

``` powershell
Loom.exe
```

Run a Loom source file:

``` powershell
Loom.exe program.loom
```

Show help:

``` powershell
Loom.exe --help
```

Show the version:

``` powershell
Loom.exe --version
```

### Option 2: Run from source

Python is required when running Loom directly from its source code.

From the project root:

``` powershell
python CLI\cli.py
```

To run a Loom file:

``` powershell
python CLI\cli.py program.loom
```

To run the REPL:

``` powershell
python REPL\repl.py
```

## Testing

Loom was developed with separate testing for the lexer, parser, and
interpreter.

The final test suite contains:

``` text
39 valid lexer tests
8 invalid lexer tests
30 valid parser tests
8 invalid parser tests
28 valid interpreter tests
6 runtime-error interpreter tests
```

This gives a total of:

``` text
119 automated tests
```

The project also includes stress testing for the lexer and parser.

### Running tests

From the project root, run the relevant test modules using Python's
module execution mode where applicable.

Example:

``` powershell
python -m Lexer.test_lexer
python -m Parser.test_parser
python -m Interpreter.test_interpreter
```

## Error Logging

Loom records errors locally without requiring a separate logging
service.

On Windows, the log file is stored at:

``` text
%LOCALAPPDATA%\Loom\loom.log
```

For example:

``` text
2026-09-24 17:52:03 | LEXER   | File: C:\Loom\Loom\CLI\cli.py | Unknown character '.'
2026-09-24 17:52:20 | RUNTIME | File: C:\Loom\Loom\bad.loom | Undefined variable or function: y
```

The log is append-only during normal operation, so previous errors
remain available for inspection.

## Version

Current release:

``` text
Loom 1.0.1
```

Check the installed version with:

``` powershell
Loom.exe --version
```

## Design Goals

Loom was designed as a compact but complete interpreted language rather
than a collection of isolated language features.

The implementation separates the major stages of execution:

``` text
Lexing
   |
Parsing
   |
AST construction
   |
Interpretation
```

This separation keeps the language implementation modular and makes
individual components easier to test and extend.

## Status

**Loom v1.0.1 is complete.**

The project includes the language implementation, testing
infrastructure, REPL, CLI, error handling, persistent logging, and a
standalone executable release.
