import os

from Lexer.Lexer import Lexer
from Parser.Parser import Parser

VALID_PATH = "test/Valid"
INVALID_PATH = "test/Invalid"
STRESS_TEST = "test/stress_test.loom"


def run_valid_tests():
    print("=" * 60)
    print("VALID TESTS")
    print("=" * 60)

    passed = 0
    failed = 0

    for filename in sorted(os.listdir(VALID_PATH)):
        if not filename.endswith(".loom"):
            continue

        print(f"\nTesting: {filename}")

        path = os.path.join(VALID_PATH, filename)

        with open(path, "r") as file:
            source = file.read()

        try:
            tokens = Lexer(source)
            parser = Parser(tokens)

            ast = parser.parse_program()
            # print(ast)

            print("[PASS]")
            passed += 1

        except Exception as e:
            print("[FAIL]")
            print(f"Reason: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"VALID TESTS COMPLETE")
    print(f"Passed : {passed}")
    print(f"Failed : {failed}")
    print("=" * 60)


def run_invalid_tests():
    print("\n")
    print("=" * 60)
    print("INVALID TESTS")
    print("=" * 60)

    passed = 0
    failed = 0

    for filename in sorted(os.listdir(INVALID_PATH)):
        if not filename.endswith(".loom"):
            continue

        print(f"\nTesting: {filename}")

        path = os.path.join(INVALID_PATH, filename)

        with open(path, "r") as file:
            source = file.read()

        try:
            tokens = Lexer(source)
            parser = Parser(tokens)

            ast = parser.parse_program()
            # print(ast)

            print("[FAIL]")
            print("Parser accepted an invalid program.")
            failed += 1

        except Exception as e:
            print("[PASS]")
            print(f"Reason: {e}")
            passed += 1

    print("\n" + "=" * 60)
    print("INVALID TESTS COMPLETE")
    print(f"Passed : {passed}")
    print(f"Failed : {failed}")
    print("=" * 60)


def run_stress_test():
    print("\n")
    print("=" * 60)
    print("STRESS TEST")
    print("=" * 60)

    with open(STRESS_TEST, "r") as file:
        source = file.read()

    try:
        tokens = Lexer(source)
        parser = Parser(tokens)

        ast = parser.parse_program()
        # print(ast)

        print("\n[PASS] stress_test.loom")

    except Exception as e:
        print("\n[FAIL] stress_test.loom")
        print(f"Reason: {e}")

    print("=" * 60)


if __name__ == "__main__":
    run_valid_tests()
    run_invalid_tests()
    run_stress_test()