import AST
import Token
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

#----------------helpers----------------------
    def peek(self):
        return self.tokens[self.current]
    
    def peek_next(self):
        if(not self.is_at_end()):
            return self.tokens[self.current+1]
        return self.peek()
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
        
        return AST.Program(statements)
        
    def parse_statement(self):
        if(self.check(Token.TokenType.PRINT)):
            return self.parse_print_statement()
        elif(self.check(Token.TokenType.RETURN)):
            return self.parse_return()
        elif(self.check(Token.TokenType.IF)):
            return self.parse_if()
        elif(self.check(Token.TokenType.WHILE)):
            return self.parse_while()
        elif(self.check(Token.TokenType.DEF)):
            return self.parse_func_def()
        elif(self.check(Token.TokenType.LBRACE)):
            return self.parse_block()
        elif(self.check(Token.TokenType.EMOTION_TAG)):
            return self.parse_emotion_tag()
        elif(self.check(Token.TokenType.NAME)):
            next = self.peek_next().type
            if(next == Token.TokenType.ASSIGN):
                return self.parse_assignment_statement()
           
            expr = self.parse_expression()
            self.consume(Token.TokenType.SEMICOLON)
            return AST.ExpressionStatement(expr)
        else: 
            raise ValueError(f"Expected: print/return/if/while/def/Block/emotion tag/variable/function call\nGot: {self.peek().value} ")
        

    def parse_print_statement(self):
        self.consume(Token.TokenType.PRINT)
        self.consume(Token.TokenType.LPAREN)
        expression = self.parse_expression()
        self.consume(Token.TokenType.RPAREN)
        self.consume(Token.TokenType.SEMICOLON)
        return AST.PrintStatement(expression)


#-------------------parse_arith()----------------------------------
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
                self.consume(Token.TokenType.RPAREN)
                return AST.FunctionCall(token.value, args)
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
        elif(self.check(Token.TokenType.PLUS)):
            op = self.consume(Token.TokenType.PLUS)
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
    
    def parse_arith(self):
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
        self.consume(Token.TokenType.ASSIGN)
        expr = self.parse_expression()
        self.consume(Token.TokenType.SEMICOLON)
        return AST.AssignStatement(var.value, expr)
    
    def parse_return(self):
        self.consume(Token.TokenType.RETURN)
        if self.check(Token.TokenType.SEMICOLON):
            self.consume(Token.TokenType.SEMICOLON)
            return AST.ReturnStatement(None)
        expr = self.parse_expression()
        self.consume(Token.TokenType.SEMICOLON)
        return AST.ReturnStatement(expr)
    
    def parse_func_def(self):
        self.consume(Token.TokenType.DEF)
        name = self.consume(Token.TokenType.NAME).value
        self.consume(Token.TokenType.LPAREN)
        args = []
        if(not self.check(Token.TokenType.RPAREN)):
            args.append(self.consume(Token.TokenType.NAME).value)

            while(self.match(Token.TokenType.COMMA)):
                args.append(self.consume(Token.TokenType.NAME).value)
        self.consume(Token.TokenType.RPAREN)
        body = self.parse_block()
        return AST.FunctionDefinition(name, args, body)
    
    def parse_block(self):
        self.consume(Token.TokenType.LBRACE)
        body = []
        while(not self.check(Token.TokenType.RBRACE) and not self.is_at_end()):
            body.append(self.parse_statement())
        
        if(self.is_at_end()): raise ValueError("Expected '}' before end of file")
        self.consume(Token.TokenType.RBRACE)
        return AST.BlockStatement(body)
    
    def parse_comparison(self):
        left = self.parse_arith()
        if(self.check(Token.TokenType.EQ) 
           or  self.check(Token.TokenType.NE)
           or  self.check(Token.TokenType.GT)
           or  self.check(Token.TokenType.LT)
           or  self.check(Token.TokenType.LE)
           or  self.check(Token.TokenType.GE)
           ):
            op = self.advance()
            right  = self.parse_arith()
            left = AST.BinaryExpression(left, op, right)

        return left
    def parse_not(self):
        if(self.check(Token.TokenType.NOT)):
            op = self.advance()
            left = self.parse_not()
            return AST.UnaryExpression(op, left)
        
        return self.parse_comparison()
    
    def parse_and(self):
        left = self.parse_not()
        while(self.check(Token.TokenType.AND)):
            op = self.advance()
            right = self.parse_not()
            left = AST.BinaryExpression(left, op, right)        
        return left

    def parse_or(self):
        left = self.parse_and()
        while self.match(Token.TokenType.OR):
            op = self.previous()
            right = self.parse_and()
            left = AST.BinaryExpression(left, op, right)
        return left

    def parse_expression(self):
        return self.parse_or()

    # INCOMPLETE FUNCS
    def parse_if(self):
        branches = self.parse_branches()
        if(self.match(Token.TokenType.ELSE)):
            else_body = self.parse_block()
            return AST.IfStatement(branches, else_body)
        return AST.IfStatement(branches)
        
    def parse_branches(self):
        branches = []
        self.consume(Token.TokenType.IF)
        self.consume(Token.TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(Token.TokenType.RPAREN)
        body = self.parse_block()
        branches.append(AST.Branch(condition, body))

        while(self.match(Token.TokenType.ELIF)):
            self.consume(Token.TokenType.LPAREN)
            condition = self.parse_expression()
            self.consume(Token.TokenType.RPAREN)
            body = self.parse_block()
            branches.append(AST.Branch(condition, body))
        return branches

    def parse_while(self):
        self.consume(Token.TokenType.WHILE)
        self.consume(Token.TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(Token.TokenType.RPAREN)
        block = self.parse_block()
        return AST.WhileStatement(condition, block)
    
    def parse_emotion_tag(self):
        emo = self.consume(Token.TokenType.EMOTION_TAG)
        statement_or_block = self.parse_statement()
        return AST.EmotionStatement(emo, statement_or_block)