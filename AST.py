
class Program:
    def __init__(self, statements):
        self.statements = statements

class Statement:
    pass

class Expression:
    pass

class AssignStatement(Statement):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
    
class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class BlockStatement(Statement):
    def __init__ (self, statements):
        self.statements = statements

class NumberLiteral(Expression):
    def __init__(self, value):
        self.value = value

class Variable(Expression):
    def __init__(self, name):
        self.name = name

class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class FunctionCall(Expression):
    def __init__(self, name, arguments, body):
        self.name = name
        self.arguments = arguments
        self.body = body

class UnaryExpression(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class ReturnStatement(Statement):
    def __init__(self, arguments):
        self.arguments = arguments

class IfCondition(Statement):
    def __init__(self, conditions, body):
        self.conditions = conditions
        self.body = body

class WhileLoop(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

