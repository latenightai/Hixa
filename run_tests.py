#!/usr/bin/env python3
"""
Simple test runner for the Hixa programming language.

This script runs basic tests without requiring pytest.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from hixa.lexer import Lexer, Token, TokenType
from hixa.parser import Parser
from hixa.ast import *
from hixa.interpreter import Interpreter


def test_lexer():
    """Test the lexical analyzer."""
    print("Testing Lexer...")
    
    # Test basic tokens
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
    
    assert len(tokens) == len(expected_types), f"Expected {len(expected_types)} tokens, got {len(tokens)}"
    for token, expected_type in zip(tokens, expected_types):
        assert token.type == expected_type, f"Expected {expected_type}, got {token.type}"
    
    print("  ✓ Basic token recognition")
    
    # Test string literals
    source = '"Hello, World!"'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 2, "Expected 2 tokens (STRING + EOF)"
    assert tokens[0].type == TokenType.STRING, "Expected STRING token"
    assert tokens[0].value == "Hello, World!", "Incorrect string value"
    
    print("  ✓ String literal tokenization")
    
    # Test numbers
    source = "42 3.14"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 3, "Expected 3 tokens (INT + FLOAT + EOF)"
    assert tokens[0].type == TokenType.INT, "Expected INT token"
    assert tokens[0].value == "42", "Incorrect int value"
    assert tokens[1].type == TokenType.FLOAT, "Expected FLOAT token"
    assert tokens[1].value == "3.14", "Incorrect float value"
    
    print("  ✓ Number tokenization")
    
    print("Lexer tests passed!")


def test_parser():
    """Test the parser."""
    print("Testing Parser...")
    
    # Test variable declaration
    source = "let x = 42;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1, "Expected 1 statement"
    statement = ast.statements[0]
    assert isinstance(statement, VariableDeclaration), "Expected VariableDeclaration"
    assert statement.name == "x", "Incorrect variable name"
    assert statement.initializer is not None, "Expected initializer"
    assert isinstance(statement.initializer, Literal), "Expected Literal initializer"
    assert statement.initializer.value == 42, "Incorrect literal value"
    
    print("  ✓ Variable declaration parsing")
    
    # Test binary expression
    source = "let result = 5 + 3;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    statement = ast.statements[0]
    assert isinstance(statement, VariableDeclaration), "Expected VariableDeclaration"
    initializer = statement.initializer
    assert isinstance(initializer, BinaryExpression), "Expected BinaryExpression"
    assert initializer.operator == "+", "Incorrect operator"
    assert isinstance(initializer.left, Literal), "Expected Literal left operand"
    assert isinstance(initializer.right, Literal), "Expected Literal right operand"
    assert initializer.left.value == 5, "Incorrect left operand"
    assert initializer.right.value == 3, "Incorrect right operand"
    
    print("  ✓ Binary expression parsing")
    
    print("Parser tests passed!")


def test_interpreter():
    """Test the interpreter."""
    print("Testing Interpreter...")
    
    # Test simple arithmetic
    source = "let x = 5 + 3; print(x);"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(ast.statements)
    
    print("  ✓ Simple arithmetic execution")
    
    # Test function call
    source = """
    fn add(a: int, b: int) -> int {
        return a + b;
    }
    let result = add(5, 3);
    print(result);
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(ast.statements)
    
    print("  ✓ Function definition and call")
    
    print("Interpreter tests passed!")


def test_examples():
    """Test the example programs."""
    print("Testing Examples...")
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("  ⚠ Examples directory not found")
        return
    
    for example_file in examples_dir.glob("*.hx"):
        print(f"  Testing {example_file.name}...")
        
        try:
            with open(example_file, 'r') as f:
                source = f.read()
            
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            if lexer.errors:
                print(f"    ❌ Lexical errors in {example_file.name}")
                continue
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            if parser.errors:
                print(f"    ❌ Parsing errors in {example_file.name}")
                continue
            
            interpreter = Interpreter()
            interpreter.interpret(ast.statements)
            
            print(f"    ✓ {example_file.name} executed successfully")
            
        except Exception as e:
            print(f"    ❌ Error in {example_file.name}: {e}")
    
    print("Examples tests completed!")


def main():
    """Run all tests."""
    print("Running Hixa Language Tests")
    print("=" * 40)
    
    try:
        test_lexer()
        print()
        
        test_parser()
        print()
        
        test_interpreter()
        print()
        
        test_examples()
        print()
        
        print("All tests passed! 🎉")
        return 0
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 