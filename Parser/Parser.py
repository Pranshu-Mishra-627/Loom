import AST
import Token
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

#----------------helpers----------------------
    def peek(self):
        return self.tokens[self.current]
    
    def advance(self):
        current_token = self.peek()
        if( not self.is_at_end()): 
            self.current+=1
        
        return current_token
    
    def is_at_end(self):
        return self.peek().type == Token.TokenType.EOF
    
    def previous(self):
        return self.tokens[self.current -1]
    
    def check(self, token_type):
        return self.peek().type == token_type

    def match(self, token_type):
        if self.check(token_type):
            self.advance()
            return True
        else: return False
    
    def consume(self, token_type):
        if not self.check(token_type):
            raise ValueError(f"Expected {token_type}, found {self.peek().value}")
        return self.advance()
#----------------------------------------------------------------

#-----------------Parser modules---------------------------------
    def parse_program(self):
        statements = []
        while(not self.is_at_end()):
            statement = self.parse_statement()
            statements.append(statement)
        
        return statements
        
    def parse_statement(self):
        if(self.check(Token.TokenType.PRINT)):
            return self.parse_print_statement()

    def parse_print_statement(self):
        self.consume(Token.TokenType.PRINT)
        self.consume(Token.TokenType.LPAREN)
        expression = self.parse_expression()
        self.consume(Token.TokenType.RPAREN)
        self.consume(Token.TokenType.SEMICOLON)
        return AST.PrintStatement(expression)


#-------------------Parse_Expression()----------------------------------
    def parse_primary(self):
        if(self.check(Token.TokenType.NUMBER)):
            token = self.consume(Token.TokenType.NUMBER)
            return AST.NumberLiteral(token.value)
        elif(self.check(Token.TokenType.STRING)):
            token = self.consume(Token.TokenType.STRING)
            return AST.StringLiteral(token.value)
        elif(self.check(Token.TokenType.NAME)):
            token = self.consume(Token.TokenType.NAME)
            if(self.check(Token.TokenType.LPAREN)):
                self.consume(Token.TokenType.LPAREN)
                args = self.parse_function_call() 
                self.match(Token.TokenType.RPAREN)
                return AST.FunctionCall(token, args)
            return AST.Variable(token.value)
        elif self.check(Token.TokenType.TRUE):
            self.consume(Token.TokenType.TRUE)
            return AST.BooleanLiteral(True)
        elif self.check(Token.TokenType.FALSE):
            self.consume(Token.TokenType.FALSE)
            return AST.BooleanLiteral(False)
        elif self.check(Token.TokenType.NONE):
            self.consume(Token.TokenType.NONE)
            return AST.NoneLiteral()
        elif self.check(Token.TokenType.LPAREN):
            self.consume(Token.TokenType.LPAREN)
            expr = self.parse_expression()
            if not self.match(Token.TokenType.RPAREN):
                raise ValueError(f"'(' was not closed")
            return expr
        else: raise ValueError(f"Expected Expression found {self.peek().type}")

    def parse_unary(self):
        if(self.check(Token.TokenType.MINUS)):
            op = self.consume(Token.TokenType.MINUS)
            operand = self.parse_unary()
            return AST.UnaryExpression(op, operand)
        elif(self.check(Token.TokenType.NOT)):
            op = self.consume(Token.TokenType.NOT)
            operand = self.parse_unary()
            return AST.UnaryExpression(op, operand)
        else: return self.parse_primary()

    def parse_term(self):
        left = self.parse_unary()
        while(self.check(Token.TokenType.STAR) 
              or self.check(Token.TokenType.SLASH)
              or self.check(Token.TokenType.MOD)
              ):
            op = self.advance()
            right = self.parse_unary()
            left = AST.BinaryExpression(left, op, right)
        return left
    
    def parse_expression(self):
        left = self.parse_term()

        while (
            self.check(Token.TokenType.PLUS)
            or self.check(Token.TokenType.MINUS)
        ):
            op = self.advance()
            right = self.parse_term()
            left = AST.BinaryExpression(left, op, right)
        return left
#----------------------------------------------------------------
    def parse_function_call(self):
        args = []

        if not self.check(Token.TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(Token.TokenType.COMMA):
                args.append(self.parse_expression())
        
        return args

    def parse_assignment_statement(self):
        var = self.consume(Token.TokenType.NAME)
        expr = self.parse_expression()
        self.consume(Token.TokenType.SEMICOLON) 
        return AST.AssignStatement(var.value, expr)
    
    def parse_return(self):
        self.consume(Token.TokenType.RETURN)
        if(self.peek().type == Token.TokenType.SEMICOLON):
            self.consume(Token.TokenType.SEMICOLON)
            return
        expr = self.parse_expression()
        return AST.ReturnStatement(expr)
    
    def parse_func_def(self):
        self.consume(Token.TokenType.DEF)
        name = self.consume(Token.TokenType.NAME).value
        self.consume(Token.TokenType.LPAREN)
        args = []
        if(not self.check(Token.TokenType.RPAREN)):
            args.append(self.consume(Token.TokenType.NAME))

            while(self.match(Token.TokenType.COMMA)):
                args.append(self.consume(Token.TokenType.NAME).value)
        self.consume(Token.TokenType.RPAREN)
        body = self.parse_program()
        return AST.FunctionDefinition(name, args, body)
        