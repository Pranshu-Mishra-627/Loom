# Loom Quick Start Guide

Welcome to Loom.

This guide is for quickly downloading, running, and testing the Loom programming language using the standalone Windows executable.

## 1. Download Loom

Download the latest `Loom.exe` from the `releases/` folder in the repository.

The executable is standalone, so you do **not** need Python or any additional dependencies to run it.

You can place `Loom.exe` anywhere on your computer.

---

## 2. Start the Loom REPL

Open PowerShell or Command Prompt in the folder containing `Loom.exe` and run:

```powershell
.\Loom.exe
```

You should see:

```text
Loom REPL v0.1
Type 'exit' to quit.

Loom>
```

The REPL allows you to enter and execute Loom code interactively.

For example:

```loom
x = 10;
y = 20;
print(x + y);
```

Output:

```text
30
```

To exit:

```text
Loom> exit
Bye!
```

---

## 3. Basic Loom Syntax

### Variables

```loom
x = 10;
name = "Loom";
active = true;
```

### Arithmetic

```loom
x = 10;
y = 5;

print(x + y);
print(x - y);
print(x * y);
print(x / y);
print(x % y);
```

### Comparisons

```loom
x = 10;

print(x > 5);
print(x == 10);
print(x != 20);
```

### Conditional Statements

```loom
x = 75;

if (x > 90) {
    print("Excellent");
} elif (x > 60) {
    print("Good");
} else {
    print("Needs improvement");
}
```

### While Loops

```loom
x = 0;

while (x < 5) {
    print(x);
    x = x + 1;
}
```

---

## 4. Functions

Functions are defined using `def`:

```loom
def add(a, b) {
    return a + b;
}

print(add(10, 20));
```

Output:

```text
30
```

Functions can also call themselves, allowing recursion.

### Recursion Example

```loom
def factorial(n) {
    if (n <= 1) {
        return 1;
    }

    return n * factorial(n - 1);
}

print(factorial(5));
```

Output:

```text
120
```

---

## 5. Annotations

Loom supports annotations using `@tag` syntax.

Example:

```loom
@debug
x = 10;
```

Annotations are metadata attached to statements.

To enable annotation output, use:

```loom
tag();

@debug
x = 10;
```

`tag()` acts as a runtime toggle for annotation output.

---

## 6. Running a Loom File

Create a file such as:

```text
hello.loom
```

with:

```loom
x = 10;
y = 20;

print(x + y);
```

Then run:

```powershell
.\Loom.exe hello.loom
```

Output:

```text
30
```

---

## 7. Useful CLI Commands

Start the REPL:

```powershell
.\Loom.exe
```

Run a Loom file:

```powershell
.\Loom.exe program.loom
```

Show help:

```powershell
.\Loom.exe --help
```

Show version:

```powershell
.\Loom.exe --version
```

Current release:

```text
Loom 1.0.1
```

---

## 8. Comments

Loom supports comments:

```loom
// This is a comment

x = 10; // This is also a comment

print(x);
```

---

## 9. Complete Example

```loom
def factorial(n) {
    if (n <= 1) {
        return 1;
    }

    return n * factorial(n - 1);
}

x = 5;

if (x > 0) {
    print("Calculating factorial...");
    print(factorial(x));
} else {
    print("Invalid number");
}
```

Output:

```text
Calculating factorial...
120
```

---

## 10. Testing Error Handling

For example:

```loom
print(y);
```

will produce a runtime error because `y` has not been defined.

Loom also records errors in a persistent local log.

On Windows:

```text
%LOCALAPPDATA%\Loom\loom.log
```

Example:

```text
2026-09-24 17:52:20 | RUNTIME | File: C:\Loom\bad.loom | Undefined variable or function: y
```

---

## 11. Quick Test Checklist

To quickly test Loom:

1. Run `Loom.exe`.
2. Try:
   ```loom
   x = 10;
   ```
3. Try:
   ```loom
   print(x * 5);
   ```
4. Try an `if` statement.
5. Try a `while` loop.
6. Define and call a function.
7. Try the factorial recursion example.
8. Try an annotation with `tag()`.
9. Run a `.loom` file directly.
10. Run:
    ```powershell
    .\Loom.exe --version
    ```
11. Try an intentional error:
    ```loom
    print(undefined_variable);
    ```
12. Check the Loom error log.

---

## 12. Exiting

To exit the REPL:

```text
Loom> exit
Bye!
```

You can now experiment with Loom directly using the standalone executable.
