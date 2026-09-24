import Token
import AST
import Errors

class ReturnSignal(Exception):
    def __init__(self, value=None):
        self.value = value

class FunctionObject:
    def __init__(self, parameters, body, parent, name):
        self.parameters = parameters
        self.body = body
        self.parent = parent
        self.name = name


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent
    def define(self, variable, value):
        self.values[variable] = value;
    def get(self, variable):
        if variable in self.values:
            return self.values[variable]
        if self.parent is not None:
            return self.parent.get(variable)
        raise Errors.LoomRuntimeError(f"Undefined variable or function: {variable}")
    
class Interpreter:
    def __init__(self, AST):
        self.globals = Environment()
        self.environment = self.globals;
        self.tags_enabled = False
        self.AST = AST
    #------------EXECUTE STATEMENTS----------------------
    def execute(self, node):
        method_name = f"execute_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)
    def execute_Program(self, node):
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result
    def execute_PrintStatement(self,node):
        value = self.evaluate(node.expression)
        print(value)
    def execute_AssignStatement(self, node):
        name = node.name
        value = self.evaluate(node.value)
        self.environment.define(name,value)

    def execute_ExpressionStatement(self, node):
        return self.evaluate(node.expression)

    def execute_BlockStatement(self,node):
        for i in node.statements :
            self.execute(i)

    def execute_IfStatement(self,node):
        for i in node.branches:
            # AST.Branch(condition, body)
            condition = self.evaluate(i.condition)
            if(condition): 
                self.execute_BlockStatement(i.body)
                return

        if node.else_block is not None:
            self.execute_BlockStatement(node.else_block)

    def execute_WhileStatement(self,node):
        while self.evaluate(node.condition):
            self.execute(node.body)
        # AST.WhileStatement(condition, body)

    def execute_ReturnStatement(self,node):
        value = None
        if node.value is not None:
            value = self.evaluate(node.value)

        if(self.environment.parent is None):
            raise Errors.LoomRuntimeError("Cannot return outside a function")
        raise ReturnSignal(value)
        #AST.ReturnStatement(value | None)

    def execute_FunctionDefinition(self,node):
        # AST.FunctionDefinition(name,parameters, body)
        funcObj = FunctionObject(node.parameters, node.body, self.environment ,node.name)
        self.environment.define(funcObj.name, funcObj)

    def execute_TagStatement(self,node):
        #AST.TagStatement()
        self.tags_enabled = not self.tags_enabled

    def execute_AnnotationStatement(self, node):
        if self.tags_enabled:
            print(f"[{node.tag_name}]: {node.tag_bodystr}")

        self.execute(node.body)

    #EVALUATE VALUES ----------------------------------
    def evaluate(self,node):
        method_name = f"evaluate_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)

    def evaluate_NumberLiteral(self, node):
        return node.value

    def evaluate_StringLiteral(self, node):
        return node.value

    def evaluate_BooleanLiteral(self, node):
        return node.value

    def evaluate_NoneLiteral(self, node):
        return None

    def evaluate_Variable(self, node):
        return self.environment.get(node.name)

    def evaluate_UnaryExpression(self,node):
        op = node.op
        operand = self.evaluate(node.operand)

        if node.op.type == Token.TokenType.PLUS:
            if not isinstance(operand, (int, float)) or isinstance(operand, bool): 
                raise Errors.LoomRuntimeError(f"Cannot apply {op} to a non-numeric operand")
            return +operand
        elif node.op.type== Token.TokenType.MINUS:
            if not isinstance(operand, (int, float)) or isinstance(operand, bool): 
                raise Errors.LoomRuntimeError(f"Cannot apply {op} to a non-numeric operand")
            return -operand
        elif node.op.type== Token.TokenType.NOT:
            return not operand
        else: raise Errors.LoomRuntimeError(f"Could not resolve unary operator: {op.type}")

    def evaluate_BinaryExpression(self, node):
        left = self.evaluate(node.left)
        op = node.op
        right = self.evaluate(node.right)

        def is_number(value):
            return isinstance(value, (int, float)) and not isinstance(value, bool)

        if op.type == Token.TokenType.STAR:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            return left * right

        elif op.type == Token.TokenType.SLASH:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            if right == 0:
                raise Errors.LoomRuntimeError("Cannot divide by zero")
            return left / right

        elif op.type == Token.TokenType.MOD:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            if right == 0:
                raise Errors.LoomRuntimeError("Cannot modulo by zero")
            return left % right

        elif op.type == Token.TokenType.PLUS:
            if is_number(left) and is_number(right):
                return left + right

            if isinstance(left, str) and isinstance(right, str):
                return left + right

            raise Errors.LoomRuntimeError(
                f"Operands for '+' must both be numbers or both be strings"
            )

        elif op.type == Token.TokenType.MINUS:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            return left - right

        elif op.type == Token.TokenType.AND:
            if not (isinstance(left, bool) and isinstance(right, bool)):
                raise Errors.LoomRuntimeError(
                    "Both operands for 'and' must be boolean"
                )
            return left and right

        elif op.type == Token.TokenType.OR:
            if not (isinstance(left, bool) and isinstance(right, bool)):
                raise Errors.LoomRuntimeError(
                    "Both operands for 'or' must be boolean"
                )
            return left or right

        elif op.type == Token.TokenType.EQ:
            return left == right

        elif op.type == Token.TokenType.NE:
            return left != right

        elif op.type == Token.TokenType.LE:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            return left <= right

        elif op.type == Token.TokenType.GE:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            return left >= right

        elif op.type == Token.TokenType.GT:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            return left > right

        elif op.type == Token.TokenType.LT:
            if not (is_number(left) and is_number(right)):
                raise Errors.LoomRuntimeError(
                    f"Both operands must be numeric for the operator {op}"
                )
            return left < right

        else:
            raise Errors.LoomRuntimeError(
                f"Could not resolve the binary operator: {op.type}"
            )

    def evaluate_FunctionCall(self, node):
        # AST.FunctionCall(name, arguments)

        func = self.environment.get(node.name)
        if not isinstance(func, FunctionObject):raise Errors.LoomRuntimeError(f"Cannot call {node.name}: Not a function")
        if len(node.arguments) != len(func.parameters):
            raise Errors.LoomRuntimeError(
                f"Expected {len(func.parameters)} arguments, "
                f"got {len(node.arguments)}, for the function {func.name}"
            )

        arguments = []
        for argument in node.arguments:
            arguments.append(self.evaluate(argument))

        oldEnv = self.environment
        tempEnv = Environment(parent=func.parent)

        for i in range(len(arguments)):
            tempEnv.define(func.parameters[i], arguments[i])

        self.environment = tempEnv

        try:
            self.execute(func.body)
            return None
        except ReturnSignal as signal:
            return signal.value
        finally:
            self.environment = oldEnv

        

