import Token
import AST

class ReturnSignal(Exception):
    def __init__(self, value=None):
        self.value = value

class FunctionObject:
    def __init__(self, parameters, body, parent, name):
        self.parameters = parameters
        self.body = body
        self.parent = parent
        self.name = name
        self.env = Environment(parent)


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent
    def define(self, variable, value):
        self.values[variable] = value;
    def get(self, variable):
        return self.values[variable]

class Interpreter:
    def __init__(self, AST):
        self.globals = Environment()
        self.environment = self.globals;
        self.AST = AST
    #------------EXECUTE STATEMENTS----------------------
    def execute(self, node):
        method_name = f"execute_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)
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

        raise ReturnSignal(value)
        #AST.ReturnStatement(value | None)

    def execute_FunctionDefinition(self,node):
        AST.FunctionDefinition()
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
            return +operand
        elif node.op.type== Token.TokenType.MINUS:
            return -operand
        elif node.op.type== Token.TokenType.NOT:
            return not operand
        else: raise ValueError(f"Could Not resolve unary operator: {op.type}")

    def evaluate_BinaryExpression(self,node):
        left = self.evaluate(node.left)
        op = node.op
        right = self.evaluate(node.right)

        if(op.type) == Token.TokenType.STAR:
            return left * right
        elif(op.type) == Token.TokenType.SLASH:
            return left/right
        elif(op.type) == Token.TokenType.MOD:
            return left % right
        elif(op.type) == Token.TokenType.PLUS:
            return left + right
        elif(op.type) == Token.TokenType.MINUS:
            return left-right
        elif(op.type) == Token.TokenType.AND:
            return left and right
        elif(op.type) == Token.TokenType.OR:
            return left or right
        elif(op.type) == Token.TokenType.EQ:
            return (left==right)
        elif(op.type) == Token.TokenType.NE:
            return left !=right
        elif(op.type) == Token.TokenType.LE:
            return left<=right
        elif(op.type) == Token.TokenType.GE:
            return left>=right
        elif(op.type) == Token.TokenType.GT:
            return left>right
        elif(op.type) == Token.TokenType.LT:
            return left<right
        else: raise ValueError(f"Could not resolve binary operator: {op.type} ")

    