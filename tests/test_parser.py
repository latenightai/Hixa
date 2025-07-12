"""
Tests for the Hixa parser.
"""

from src.hixa.lexer import Lexer
from src.hixa.parser import Parser
from src.hixa.ast import *


class TestParser:
    """Test cases for the parser."""
    
    def test_variable_declaration(self):
        """Test parsing variable declarations."""
        source = "let x = 42;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        statement = ast.statements[0]
        assert isinstance(statement, VariableDeclaration)
        assert statement.name == "x"
        assert statement.initializer is not None
        assert isinstance(statement.initializer, Literal)
        assert statement.initializer.value == 42
    
    def test_function_declaration(self):
        """Test parsing function declarations."""
        source = "fn add(a: int, b: int) -> int { return a + b; }"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        statement = ast.statements[0]
        assert isinstance(statement, FunctionDeclaration)
        assert statement.name == "add"
        assert len(statement.parameters) == 2
        assert statement.parameters[0].name == "a"
        assert statement.parameters[1].name == "b"
        assert statement.return_type == "int"
    
    def test_binary_expression(self):
        """Test parsing binary expressions."""
        source = "let result = 5 + 3;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        statement = ast.statements[0]
        assert isinstance(statement, VariableDeclaration)
        initializer = statement.initializer
        assert isinstance(initializer, BinaryExpression)
        assert initializer.operator == "+"
        assert isinstance(initializer.left, Literal)
        assert isinstance(initializer.right, Literal)
        assert initializer.left.value == 5
        assert initializer.right.value == 3
    
    def test_if_statement(self):
        """Test parsing if statements."""
        source = "if x > 0 { print(x); } else { print(0); }"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        statement = ast.statements[0]
        assert isinstance(statement, IfStatement)
        assert isinstance(statement.condition, BinaryExpression)
        assert statement.condition.operator == ">"
        assert statement.then_branch is not None
        assert statement.else_branch is not None
    
    def test_while_statement(self):
        """Test parsing while statements."""
        source = "while i > 0 { i = i - 1; }"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        statement = ast.statements[0]
        assert isinstance(statement, WhileStatement)
        assert isinstance(statement.condition, BinaryExpression)
        assert statement.condition.operator == ">"
        assert statement.body is not None
    
    def test_array_expression(self):
        """Test parsing array expressions."""
        source = "let arr = [1, 2, 3];"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        statement = ast.statements[0]
        assert isinstance(statement, VariableDeclaration)
        initializer = statement.initializer
        assert isinstance(initializer, ArrayExpression)
        assert len(initializer.elements) == 3
        for i, element in enumerate(initializer.elements):
            assert isinstance(element, Literal)
            assert element.value == i + 1
    
    def test_object_expression(self):
        """Test parsing object expressions."""
        source = "let obj = { name: \"John\", age: 30 };"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        statement = ast.statements[0]
        assert isinstance(statement, VariableDeclaration)
        initializer = statement.initializer
        assert isinstance(initializer, ObjectExpression)
        assert len(initializer.properties) == 2
        assert initializer.properties[0].key == "name"
        assert initializer.properties[1].key == "age"
    
    def test_call_expression(self):
        """Test parsing function calls."""
        source = "let result = add(5, 3);"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        statement = ast.statements[0]
        assert isinstance(statement, VariableDeclaration)
        initializer = statement.initializer
        assert isinstance(initializer, CallExpression)
        assert isinstance(initializer.callee, Identifier)
        assert initializer.callee.name == "add"
        assert len(initializer.arguments) == 2
    
    def test_error_recovery(self):
        """Test parser error recovery."""
        source = "let x = 42; let y = ; let z = 10;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Should recover and parse valid statements
        assert len(ast.statements) >= 1
        assert len(parser.errors) > 0


class TestASTNodes:
    """Test cases for AST node classes."""
    
    def test_literal_node(self):
        """Test Literal AST node."""
        literal = Literal(42, "int")
        assert literal.value == 42
        assert literal.type_ == "int"
    
    def test_identifier_node(self):
        """Test Identifier AST node."""
        identifier = Identifier("x")
        assert identifier.name == "x"
    
    def test_binary_expression_node(self):
        """Test BinaryExpression AST node."""
        left = Literal(5, "int")
        right = Literal(3, "int")
        binary = BinaryExpression(left, "+", right)
        assert binary.left == left
        assert binary.right == right
        assert binary.operator == "+"
    
    def test_variable_declaration_node(self):
        """Test VariableDeclaration AST node."""
        initializer = Literal(42, "int")
        decl = VariableDeclaration("x", "int", initializer)
        assert decl.name == "x"
        assert decl.type_annotation == "int"
        assert decl.initializer == initializer
    
    def test_function_declaration_node(self):
        """Test FunctionDeclaration AST node."""
        body = BlockStatement([])
        func = FunctionDeclaration("add", [], "int", body)
        assert func.name == "add"
        assert func.return_type == "int"
        assert func.body == body 