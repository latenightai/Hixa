"""
Hixa Programming Language

A modern, production-ready programming language implemented in Python.
"""

__version__ = "0.1.0"
__author__ = "Hixa Language Team"
__email__ = "team@hixa-lang.org"

from .lexer import Lexer, Token, TokenType
from .parser import Parser
from .ast import *
from .interpreter import Interpreter
from .types import *
from .stdlib import StandardLibrary

__all__ = [
    "Lexer",
    "Parser", 
    "Interpreter",
    "StandardLibrary",
    "Token",
    "TokenType",
    # AST nodes
    "Program",
    "FunctionDeclaration",
    "VariableDeclaration",
    "BinaryExpression",
    "UnaryExpression",
    "Literal",
    "Identifier",
    "CallExpression",
    "BlockStatement",
    "IfStatement",
    "WhileStatement",
    "ForStatement",
    "ReturnStatement",
    "AssignmentExpression",
    "MemberExpression",
    "ArrayExpression",
    "ObjectExpression",
    "IndexExpression",
    # Types
    "HixaType",
    "IntType",
    "FloatType", 
    "StringType",
    "BooleanType",
    "ArrayType",
    "ObjectType",
    "FunctionType",
    "VoidType",
] 