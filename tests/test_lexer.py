"""
Tests for the Hixa lexer.
"""

import pytest
from src.hixa.lexer import Lexer, Token, TokenType


class TestLexer:
    """Test cases for the lexical analyzer."""
    
    def test_basic_tokens(self):
        """Test basic token recognition."""
        source = "let x = 42;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.LET,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN,
            TokenType.INT,
            TokenType.SEMICOLON,
            TokenType.EOF
        ]
        
        assert len(tokens) == len(expected_types)
        for token, expected_type in zip(tokens, expected_types):
            assert token.type == expected_type
    
    def test_string_literals(self):
        """Test string literal tokenization."""
        source = '"Hello, World!"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 2  # STRING + EOF
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "Hello, World!"
    
    def test_numbers(self):
        """Test number tokenization."""
        source = "42 3.14"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 3  # INT + FLOAT + EOF
        assert tokens[0].type == TokenType.INT
        assert tokens[0].value == "42"
        assert tokens[1].type == TokenType.FLOAT
        assert tokens[1].value == "3.14"
    
    def test_operators(self):
        """Test operator tokenization."""
        source = "+ - * / % == != < <= > >="
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected_operators = ["+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">="]
        assert len(tokens) == len(expected_operators) + 1  # +1 for EOF
        
        for token, expected_op in zip(tokens[:-1], expected_operators):
            assert token.value == expected_op
    
    def test_keywords(self):
        """Test keyword recognition."""
        source = "let fn if else while for return"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected_keywords = [
            TokenType.LET,
            TokenType.FN,
            TokenType.IF,
            TokenType.ELSE,
            TokenType.WHILE,
            TokenType.FOR,
            TokenType.RETURN
        ]
        
        assert len(tokens) == len(expected_keywords) + 1  # +1 for EOF
        for token, expected_type in zip(tokens[:-1], expected_keywords):
            assert token.type == expected_type
    
    def test_identifiers(self):
        """Test identifier tokenization."""
        source = "variable_name _underscore camelCase"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected_identifiers = ["variable_name", "_underscore", "camelCase"]
        assert len(tokens) == len(expected_identifiers) + 1  # +1 for EOF
        
        for token, expected_id in zip(tokens[:-1], expected_identifiers):
            assert token.type == TokenType.IDENTIFIER
            assert token.value == expected_id
    
    def test_comments(self):
        """Test comment handling."""
        source = "// This is a comment\nlet x = 42;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Should have: LET, IDENTIFIER, ASSIGN, INT, SEMICOLON, EOF
        assert len(tokens) == 6
        assert tokens[0].type == TokenType.LET
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[2].type == TokenType.ASSIGN
        assert tokens[3].type == TokenType.INT
        assert tokens[4].type == TokenType.SEMICOLON
        assert tokens[5].type == TokenType.EOF
    
    def test_boolean_literals(self):
        """Test boolean literal tokenization."""
        source = "true false"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 3  # BOOLEAN + BOOLEAN + EOF
        assert tokens[0].type == TokenType.BOOLEAN
        assert tokens[0].value == "true"
        assert tokens[1].type == TokenType.BOOLEAN
        assert tokens[1].value == "false"
    
    def test_error_handling(self):
        """Test error handling for invalid characters."""
        source = "let x = @;"
        lexer = Lexer(source)
        
        with pytest.raises(SyntaxError):
            lexer.tokenize()


class TestToken:
    """Test cases for Token class."""
    
    def test_token_creation(self):
        """Test token creation and attributes."""
        token = Token(TokenType.IDENTIFIER, "x", 1, 1)
        
        assert token.type == TokenType.IDENTIFIER
        assert token.value == "x"
        assert token.line == 1
        assert token.column == 1
    
    def test_token_equality(self):
        """Test token equality."""
        token1 = Token(TokenType.IDENTIFIER, "x", 1, 1)
        token2 = Token(TokenType.IDENTIFIER, "x", 1, 1)
        token3 = Token(TokenType.INT, "42", 1, 1)
        
        assert token1 == token2
        assert token1 != token3
    
    def test_token_repr(self):
        """Test token string representation."""
        token = Token(TokenType.IDENTIFIER, "x", 1, 1)
        repr_str = repr(token)
        
        assert "Token" in repr_str
        assert "IDENTIFIER" in repr_str
        assert "x" in repr_str
        assert "line=1" in repr_str
        assert "col=1" in repr_str 