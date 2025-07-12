"""
Abstract Syntax Tree (AST) for the Hixa programming language.

This module defines all AST node types that represent the structure
of Hixa source code after parsing.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from dataclasses import dataclass


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Accept a visitor for this node."""
        pass


class ASTVisitor(ABC):
    """Base class for AST visitors."""
    
    @abstractmethod
    def visit_program(self, node: 'Program') -> Any:
        pass
    
    @abstractmethod
    def visit_function_declaration(self, node: 'FunctionDeclaration') -> Any:
        pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: 'VariableDeclaration') -> Any:
        pass
    
    @abstractmethod
    def visit_binary_expression(self, node: 'BinaryExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_unary_expression(self, node: 'UnaryExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: 'Literal') -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: 'Identifier') -> Any:
        pass
    
    @abstractmethod
    def visit_call_expression(self, node: 'CallExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_block_statement(self, node: 'BlockStatement') -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: 'IfStatement') -> Any:
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: 'WhileStatement') -> Any:
        pass
    
    @abstractmethod
    def visit_for_statement(self, node: 'ForStatement') -> Any:
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: 'ReturnStatement') -> Any:
        pass
    
    @abstractmethod
    def visit_assignment_expression(self, node: 'AssignmentExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_member_expression(self, node: 'MemberExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_array_expression(self, node: 'ArrayExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_object_expression(self, node: 'ObjectExpression') -> Any:
        pass
    
    @abstractmethod
    def visit_index_expression(self, node: 'IndexExpression') -> Any:
        pass


# Program and Declarations
@dataclass
class Program(ASTNode):
    """Represents a complete program."""
    statements: List[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_program(self)


@dataclass
class FunctionDeclaration(ASTNode):
    """Represents a function declaration."""
    name: str
    parameters: List['Parameter']
    return_type: Optional[str]
    body: 'BlockStatement'
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_function_declaration(self)


@dataclass
class Parameter:
    """Represents a function parameter."""
    name: str
    type_annotation: Optional[str]


@dataclass
class VariableDeclaration(ASTNode):
    """Represents a variable declaration."""
    name: str
    type_annotation: Optional[str]
    initializer: Optional[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_variable_declaration(self)


# Expressions
@dataclass
class BinaryExpression(ASTNode):
    """Represents a binary expression."""
    left: ASTNode
    operator: str
    right: ASTNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_binary_expression(self)


@dataclass
class UnaryExpression(ASTNode):
    """Represents a unary expression."""
    operator: str
    operand: ASTNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_unary_expression(self)


@dataclass
class Literal(ASTNode):
    """Represents a literal value."""
    value: Any
    type_: str  # 'int', 'float', 'string', 'boolean', 'null'
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_literal(self)


@dataclass
class Identifier(ASTNode):
    """Represents an identifier."""
    name: str
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_identifier(self)


@dataclass
class CallExpression(ASTNode):
    """Represents a function call."""
    callee: ASTNode
    arguments: List[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_call_expression(self)


@dataclass
class AssignmentExpression(ASTNode):
    """Represents an assignment expression."""
    target: ASTNode
    operator: str  # '=', '+=', '-=', etc.
    value: ASTNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_assignment_expression(self)


@dataclass
class MemberExpression(ASTNode):
    """Represents a member access expression (e.g., obj.property)."""
    object_: ASTNode
    property: ASTNode
    computed: bool  # True for obj[prop], False for obj.prop
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_member_expression(self)


@dataclass
class ArrayExpression(ASTNode):
    """Represents an array literal."""
    elements: List[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_array_expression(self)


@dataclass
class ObjectExpression(ASTNode):
    """Represents an object literal."""
    properties: List['Property']
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_object_expression(self)


@dataclass
class Property:
    """Represents an object property."""
    key: str
    value: ASTNode


@dataclass
class IndexExpression(ASTNode):
    """Represents an array index access."""
    array: ASTNode
    index: ASTNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_index_expression(self)


# Statements
@dataclass
class BlockStatement(ASTNode):
    """Represents a block of statements."""
    statements: List[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_block_statement(self)


@dataclass
class IfStatement(ASTNode):
    """Represents an if statement."""
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_if_statement(self)


@dataclass
class WhileStatement(ASTNode):
    """Represents a while loop."""
    condition: ASTNode
    body: ASTNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_while_statement(self)


@dataclass
class ForStatement(ASTNode):
    """Represents a for loop."""
    initializer: Optional[ASTNode]
    condition: Optional[ASTNode]
    increment: Optional[ASTNode]
    body: ASTNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_for_statement(self)


@dataclass
class ReturnStatement(ASTNode):
    """Represents a return statement."""
    value: Optional[ASTNode]
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_return_statement(self) 