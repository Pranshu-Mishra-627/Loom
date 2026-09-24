LOOM CURRENT INTERPRETER TEST SUITE
===================================

This suite targets the CURRENT interpreter only.
Emotion annotations are intentionally excluded.

Run each file through your normal Lexer -> Parser -> Interpreter pipeline.

VALID TESTS
01_literals.loom             literals, print
02_assignment.loom           assignment and variable lookup
03_arithmetic.loom           + - * / % and precedence
04_unary.loom                unary + - not
05_comparison.loom           == != < > <= >=
06_logical.loom              and / or / not
07_parentheses.loom          grouping and precedence
08_expression_statement.loom variable-started expression statements
09_if.loom                   if
10_if_elif.loom              if / elif / else
11_while.loom                while loop
12_nested_control.loom       nested if / while
13_function_basic.loom       basic function + return
14_function_locals.loom      local variables and return
15_function_global_lookup.loom function reading global variable
16_function_shadowing.loom  local variable does not overwrite global
17_function_multiple_calls.loom fresh env per call
18_function_none_return.loom function with no explicit return
19_function_return_empty.loom return;
20_function_return_in_if.loom return propagating through if
21_function_return_in_while.loom return propagating through while
22_function_expression_args.loom arguments are expressions
23_function_nested_calls.loom function calls as arguments
24_recursion_factorial.loom recursion
25_recursion_fibonacci.loom recursion with multiple calls
26_nested_function.loom function defined inside function
27_parameter_count.loom valid multi-parameter call
28_mixed_runtime.loom larger integrated program

RUNTIME ERROR TESTS
These should fail at runtime, not silently succeed.

01_undefined_variable.loom
02_division_by_zero.loom
03_wrong_argument_count_too_few.loom
04_wrong_argument_count_too_many.loom
05_return_at_top_level.loom
06_call_non_function.loom

Note: 5 + 3; as a top-level standalone expression is NOT included because the
current Parser.parse_statement() only accepts expression statements beginning
with NAME. A test such as x + 3; is included instead.
