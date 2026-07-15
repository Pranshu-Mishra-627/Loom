class Program:
    def __init__(self, statements):
        self.statements = statements


class Statement:
    pass


class Expression:
    pass


class AssignStatement(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ReturnStatement(Statement):
    def __init__(self, value=None):
        self.value = value


class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class EmotionStatement(Statement):
    def __init__(self, emotion, body):
        self.emotion = emotion
        self.body = body


class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements


class IfStatement(Statement):
    def __init__(self, branches, else_block=None):
        self.branches = branches
        self.else_block = else_block

class Branch():
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class FunctionDefinition(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


class NumberLiteral(Expression):
    def __init__(self, value):
        self.value = value


class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value


class BooleanLiteral(Expression):
    def __init__(self, value):
        self.value = value


class NoneLiteral(Expression):
    pass


class Variable(Expression):
    def __init__(self, name):
        self.name = name


class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryExpression(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class FunctionCall(Expression):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments