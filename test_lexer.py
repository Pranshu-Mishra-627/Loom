from pathlib import Path
from Lexer import Lexer

VALID_DIR = Path("test/Valid")
INVALID_DIR = Path("test/Invalid")

passed = 0
failed = 0


def run_valid_tests():
    global passed, failed

    print("\n========== VALID TESTS ==========\n")

    for file in sorted(VALID_DIR.glob("*.loom")):
        print(f"Testing {file.name}...")

        try:
            source = file.read_text(encoding="utf-8")
            tokens = Lexer(source)

            print("PASS")

            # Uncomment these if you want to see every token
            # for token in tokens:
            #     print(token)

            passed += 1

        except Exception as e:
            print(f"FAIL -> {e}")
            failed += 1

        print()


def run_invalid_tests():
    global passed, failed

    print("\n========== INVALID TESTS ==========\n")

    for file in sorted(INVALID_DIR.glob("*.loom")):
        print(f"Testing {file.name}...")

        try:
            source = file.read_text(encoding="utf-8")
            Lexer(source)

            print("FAIL (Lexer should have thrown an error)")
            failed += 1

        except Exception:
            print("PASS (Correctly rejected)")
            passed += 1

        print()


def run_stress_test():
    global passed, failed

    print("\n========== STRESS TEST ==========\n")

    try:
        source = Path("test/stress_test.loom").read_text(encoding="utf-8")
        Lexer(source)

        print("PASS")
        passed += 1

    except Exception as e:
        print(f"FAIL -> {e}")
        failed += 1


run_valid_tests()
run_invalid_tests()
run_stress_test()

print("\n==============================")
print(f"Passed : {passed}")
print(f"Failed : {failed}")
print("==============================")