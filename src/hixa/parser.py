"""
Parser for the Hixa programming language.

This module handles parsing of tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional
from .lexer import Token, TokenType
from .ast import *


class Parser:
    """Parser for Hixa source code."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors: List[str] = []
    
    def parse(self) -> Program:
        """Parse tokens into an AST."""
        statements = []
        
        while not self.is_at_end():
            try:
                statement = self.declaration()
                if statement:
                    statements.append(statement)
            except Exception as e:
                self.errors.append(str(e))
                self.synchronize()
        
        return Program(statements)
    
    def declaration(self) -> Optional[ASTNode]:
        """Parse a declaration (function, variable, etc.)."""
        try:
            if self.match(TokenType.FN) or self.match(TokenType.KAM):
                return self.function_declaration()
            elif self.match(TokenType.LET) or self.match(TokenType.DHORA):
                return self.variable_declaration()
            else:
                return self.statement()
        except Exception as e:
            self.errors.append(f"Error parsing declaration: {e}")
            self.synchronize()
            return None
    
    def function_declaration(self) -> FunctionDeclaration:
        """Parse a function declaration."""
        self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = self.previous().value
        
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        parameters = self.parameters()
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        
        return_type = None
        if self.match(TokenType.ARROW):
            self.consume(TokenType.IDENTIFIER, "Expected return type")
            return_type = self.previous().value
        
        # Allow newlines after '{'
        self.consume(TokenType.LBRACE, "Expected '{' before function body")
        while self.match(TokenType.NEWLINE):
            pass
        body = self.block_statement()
        
        return FunctionDeclaration(name, parameters, return_type, body)
    
    def parameters(self) -> List[Parameter]:
        """Parse function parameters."""
        parameters = []
        
        if not self.check(TokenType.RPAREN):
            while True:
                self.consume(TokenType.IDENTIFIER, "Expected parameter name")
                name = self.previous().value
                
                type_annotation = None
                if self.match(TokenType.COLON):
                    self.consume(TokenType.IDENTIFIER, "Expected parameter type")
                    type_annotation = self.previous().value
                
                parameters.append(Parameter(name, type_annotation))
                
                if not self.match(TokenType.COMMA):
                    break
        
        return parameters
    
    def variable_declaration(self) -> VariableDeclaration:
        """Parse a variable declaration."""
        self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = self.previous().value
        
        type_annotation = None
        if self.match(TokenType.COLON):
            self.consume(TokenType.IDENTIFIER, "Expected variable type")
            type_annotation = self.previous().value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        
        # Accept semicolon, newline, or EOF as statement terminator
        if self.match(TokenType.SEMICOLON) or self.check(TokenType.EOF) or self.check(TokenType.NEWLINE):
            self.advance() if not self.check(TokenType.EOF) else None
        else:
            raise self.error(self.peek(), "Expected ';' or newline after variable declaration")
        
        return VariableDeclaration(name, type_annotation, initializer)
    
    def statement(self) -> ASTNode:
        """Parse a statement."""
        if self.match(TokenType.IF) or self.match(TokenType.JODI):
            return self.if_statement()
        elif self.match(TokenType.WHILE) or self.match(TokenType.JETIALOIKE):
            return self.while_statement()
        elif self.match(TokenType.FOR) or self.match(TokenType.KARONE):
            return self.for_statement()
        elif self.match(TokenType.RETURN) or self.match(TokenType.GHAURAI_DIYA):
            return self.return_statement()
        elif self.match(TokenType.LBRACE):
            return self.block_statement()
        else:
            return self.expression_statement()
    
    def if_statement(self) -> IfStatement:
        """Parse an if statement."""
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after if condition")
        
        then_branch = self.statement()
        else_branch = None
        
        if self.match(TokenType.ELSE) or self.match(TokenType.NOHOLE):
            else_branch = self.statement()
        
        return IfStatement(condition, then_branch, else_branch)
    
    def while_statement(self) -> WhileStatement:
        """Parse a while statement."""
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after while condition")
        
        body = self.statement()
        
        return WhileStatement(condition, body)
    
    def for_statement(self) -> ForStatement:
        """Parse a for statement."""
        self.consume(TokenType.LPAREN, "Expected '(' after 'for'")
        
        initializer = None
        if not self.match(TokenType.SEMICOLON):
            if self.match(TokenType.LET) or self.match(TokenType.DHORA):
                initializer = self.variable_declaration()
            else:
                initializer = self.expression_statement()
        
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after for loop condition")
        
        increment = None
        if not self.check(TokenType.RPAREN):
            increment = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after for clauses")
        
        body = self.statement()
        
        return ForStatement(initializer, condition, increment, body)
    
    def return_statement(self) -> ReturnStatement:
        """Parse a return statement."""
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expected ';' after return value")
        
        return ReturnStatement(value)
    
    def block_statement(self) -> BlockStatement:
        """Parse a block statement."""
        statements = []
        
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            # Skip newlines between statements
            while self.match(TokenType.NEWLINE):
                pass
            if self.check(TokenType.RBRACE) or self.is_at_end():
                break
            statement = self.declaration()
            if statement:
                statements.append(statement)
        
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        
        return BlockStatement(statements)
    
    def expression_statement(self) -> ASTNode:
        """Parse an expression statement."""
        expr = self.expression()
        # Accept semicolon, newline, or EOF as statement terminator
        if self.match(TokenType.SEMICOLON):
            pass  # Semicolon consumed
        elif self.check(TokenType.EOF) or self.check(TokenType.NEWLINE):
            self.advance() if not self.check(TokenType.EOF) else None
        else:
            raise self.error(self.peek(), "Expected ';' or newline after expression")
        return expr
    
    def expression(self) -> ASTNode:
        """Parse an expression."""
        return self.assignment()
    
    def assignment(self) -> ASTNode:
        """Parse an assignment expression."""
        expr = self.or_expression()
        
        if self.match(TokenType.ASSIGN):
            equals = self.previous()
            value = self.assignment()
            
            if isinstance(expr, Identifier):
                return AssignmentExpression(expr, equals.value, value)
            elif isinstance(expr, MemberExpression):
                return AssignmentExpression(expr, equals.value, value)
            
            self.error(equals, "Invalid assignment target")
        
        return expr
    
    def or_expression(self) -> ASTNode:
        """Parse an OR expression."""
        expr = self.and_expression()
        
        while self.match(TokenType.OR, TokenType.BA):
            operator = self.previous()
            right = self.and_expression()
            expr = BinaryExpression(expr, operator.value, right)
        
        return expr
    
    def and_expression(self) -> ASTNode:
        """Parse an AND expression."""
        expr = self.equality()
        
        while self.match(TokenType.AND, TokenType.ARU):
            operator = self.previous()
            right = self.equality()
            expr = BinaryExpression(expr, operator.value, right)
        
        return expr
    
    def equality(self) -> ASTNode:
        """Parse an equality expression."""
        expr = self.comparison()
        
        while self.match(TokenType.NOT_EQUAL, TokenType.EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpression(expr, operator.value, right)
        
        return expr
    
    def comparison(self) -> ASTNode:
        """Parse a comparison expression."""
        expr = self.term()
        
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, 
                        TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpression(expr, operator.value, right)
        
        return expr
    
    def term(self) -> ASTNode:
        """Parse a term expression."""
        expr = self.factor()
        
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpression(expr, operator.value, right)
        
        return expr
    
    def factor(self) -> ASTNode:
        """Parse a factor expression."""
        expr = self.unary()
        
        while self.match(TokenType.DIVIDE, TokenType.MULTIPLY, TokenType.MODULO):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpression(expr, operator.value, right)
        
        return expr
    
    def unary(self) -> ASTNode:
        """Parse a unary expression."""
        if self.match(TokenType.NOT, TokenType.NOT_KORA, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpression(operator.value, right)
        
        return self.call()
    
    def call(self) -> ASTNode:
        """Parse a call expression."""
        expr = self.primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                self.consume(TokenType.IDENTIFIER, "Expected property name after '.'")
                name = self.previous()
                expr = MemberExpression(expr, Identifier(name.value), False)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after array index")
                expr = IndexExpression(expr, index)
            else:
                break
        
        return expr

    def finish_call(self, callee: ASTNode) -> CallExpression:
        """Finish parsing a call expression."""
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        paren = self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        
        return CallExpression(callee, arguments)
    
    def primary(self) -> ASTNode:
        """Parse a primary expression."""
        if self.match(TokenType.FALSE, TokenType.MISA):
            return Literal(False, "boolean")
        elif self.match(TokenType.TRUE, TokenType.HOSA):
            return Literal(True, "boolean")
        elif self.match(TokenType.NULL, TokenType.NAI):
            return Literal(None, "null")
        
        if self.match(TokenType.INT):
            return Literal(int(self.previous().value), "int")
        elif self.match(TokenType.FLOAT):
            return Literal(float(self.previous().value), "float")
        elif self.match(TokenType.STRING):
            return Literal(self.previous().value, "string")
        
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().value)
        
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        if self.match(TokenType.LBRACKET):
            return self.array_expression()
        
        if self.match(TokenType.LBRACE):
            return self.object_expression()
        
        raise self.error(self.peek(), "Expected expression")
    
    def array_expression(self) -> ArrayExpression:
        """Parse an array expression."""
        elements = []
        
        if not self.check(TokenType.RBRACKET):
            while True:
                elements.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        
        self.consume(TokenType.RBRACKET, "Expected ']' after array elements")
        
        return ArrayExpression(elements)
    
    def object_expression(self) -> ObjectExpression:
        """Parse an object expression."""
        properties = []
        
        if not self.check(TokenType.RBRACE):
            while True:
                self.consume(TokenType.IDENTIFIER, "Expected property name")
                name = self.previous().value
                
                self.consume(TokenType.COLON, "Expected ':' after property name")
                value = self.expression()
                
                properties.append(Property(name, value))
                
                if not self.match(TokenType.COMMA):
                    break
        
        self.consume(TokenType.RBRACE, "Expected '}' after object properties")
        
        return ObjectExpression(properties)
    
    # Helper methods
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False
    
    def check(self, type_: TokenType) -> bool:
        """Check if current token is of the given type."""
        if self.is_at_end():
            return False
        return self.peek().type == type_
    
    def advance(self) -> Token:
        """Advance to next token."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of tokens."""
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        """Get current token without advancing."""
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        """Get previous token."""
        return self.tokens[self.current - 1]
    
    def consume(self, type_: TokenType, message: str) -> Token:
        """Consume a token of expected type."""
        if self.check(type_):
            return self.advance()
        
        raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str) -> Exception:
        """Create a parsing error."""
        error_msg = f"Error at line {token.line}, column {token.column}: {message}"
        self.errors.append(error_msg)
        return SyntaxError(error_msg)
    
    def synchronize(self):
        """Synchronize parser after error."""
        self.advance()
        
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            if self.peek().type in [
                # English keywords
                TokenType.FN, TokenType.LET, TokenType.IF, TokenType.WHILE,
                TokenType.FOR, TokenType.RETURN,
                # Assamese keywords
                TokenType.KAM, TokenType.DHORA, TokenType.JODI, TokenType.JETIALOIKE,
                TokenType.KARONE, TokenType.GHAURAI_DIYA
            ]:
                return
            
            self.advance() 