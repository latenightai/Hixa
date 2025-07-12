"""
Type system for the Hixa programming language.

This module defines the type system, type checking, and type inference
capabilities for the Hixa language.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass


class HixaType(ABC):
    """Base class for all Hixa types."""
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    
    @abstractmethod
    def is_assignable_from(self, other: 'HixaType') -> bool:
        """Check if a value of type 'other' can be assigned to this type."""
        pass


@dataclass
class IntType(HixaType):
    """Integer type."""
    
    def __str__(self) -> str:
        return "int"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, IntType)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return isinstance(other, IntType)


@dataclass
class FloatType(HixaType):
    """Float type."""
    
    def __str__(self) -> str:
        return "float"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, FloatType)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return isinstance(other, (IntType, FloatType))


@dataclass
class StringType(HixaType):
    """String type."""
    
    def __str__(self) -> str:
        return "string"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, StringType)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return isinstance(other, StringType)


@dataclass
class BooleanType(HixaType):
    """Boolean type."""
    
    def __str__(self) -> str:
        return "boolean"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, BooleanType)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return isinstance(other, BooleanType)


@dataclass
class ArrayType(HixaType):
    """Array type."""
    element_type: HixaType
    
    def __str__(self) -> str:
        return f"[{self.element_type}]"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, ArrayType) and self.element_type == other.element_type
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return isinstance(other, ArrayType) and self.element_type.is_assignable_from(other.element_type)


@dataclass
class ObjectType(HixaType):
    """Object type."""
    properties: Dict[str, HixaType]
    
    def __str__(self) -> str:
        props = ", ".join(f"{k}: {v}" for k, v in self.properties.items())
        return f"{{{props}}}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ObjectType):
            return False
        return self.properties == other.properties
    
    def is_assignable_from(self, other: HixaType) -> bool:
        if not isinstance(other, ObjectType):
            return False
        
        # Check if all required properties exist and are compatible
        for prop_name, prop_type in self.properties.items():
            if prop_name not in other.properties:
                return False
            if not prop_type.is_assignable_from(other.properties[prop_name]):
                return False
        
        return True


@dataclass
class FunctionType(HixaType):
    """Function type."""
    parameter_types: List[HixaType]
    return_type: HixaType
    
    def __str__(self) -> str:
        params = ", ".join(str(t) for t in self.parameter_types)
        return f"({params}) -> {self.return_type}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionType):
            return False
        return (self.parameter_types == other.parameter_types and 
                self.return_type == other.return_type)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        if not isinstance(other, FunctionType):
            return False
        
        # Check parameter count
        if len(self.parameter_types) != len(other.parameter_types):
            return False
        
        # Check parameter types (contravariant)
        for self_param, other_param in zip(self.parameter_types, other.parameter_types):
            if not other_param.is_assignable_from(self_param):
                return False
        
        # Check return type (covariant)
        return self.return_type.is_assignable_from(other.return_type)


@dataclass
class VoidType(HixaType):
    """Void type (for functions that don't return anything)."""
    
    def __str__(self) -> str:
        return "void"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, VoidType)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return isinstance(other, VoidType)


@dataclass
class UnionType(HixaType):
    """Union type (e.g., int | string)."""
    types: List[HixaType]
    
    def __str__(self) -> str:
        return " | ".join(str(t) for t in self.types)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, UnionType):
            return False
        return set(self.types) == set(other.types)
    
    def is_assignable_from(self, other: HixaType) -> bool:
        return any(t.is_assignable_from(other) for t in self.types)


class TypeChecker:
    """Type checker for Hixa programs."""
    
    def __init__(self):
        self.scope_stack: List[Dict[str, HixaType]] = [{}]
        self.functions: Dict[str, FunctionType] = {}
        self.errors: List[str] = []
    
    def check_program(self, program) -> bool:
        """Type check a complete program."""
        self.errors.clear()
        
        # First pass: collect function signatures
        for statement in program.statements:
            if hasattr(statement, 'name') and hasattr(statement, 'parameters'):
                # This is a function declaration
                param_types = []
                for param in statement.parameters:
                    param_type = self._parse_type_annotation(param.type_annotation)
                    param_types.append(param_type)
                
                return_type = self._parse_type_annotation(statement.return_type)
                if return_type is None:
                    return_type = VoidType()
                
                self.functions[statement.name] = FunctionType(param_types, return_type)
        
        # Second pass: type check all statements
        for statement in program.statements:
            self._check_statement(statement)
        
        return len(self.errors) == 0
    
    def _check_statement(self, statement) -> Optional[HixaType]:
        """Type check a statement."""
        if hasattr(statement, 'accept'):
            return statement.accept(self)
        return None
    
    def _check_expression(self, expression) -> Optional[HixaType]:
        """Type check an expression."""
        if hasattr(expression, 'accept'):
            return expression.accept(self)
        return None
    
    def _parse_type_annotation(self, annotation: Optional[str]) -> Optional[HixaType]:
        """Parse a type annotation string into a HixaType."""
        if annotation is None:
            return None
        
        type_map = {
            'int': IntType(),
            'float': FloatType(),
            'string': StringType(),
            'boolean': BooleanType(),
            'void': VoidType(),
        }
        
        return type_map.get(annotation)
    
    def _enter_scope(self):
        """Enter a new scope."""
        self.scope_stack.append({})
    
    def _exit_scope(self):
        """Exit the current scope."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
    
    def _declare_variable(self, name: str, type_: HixaType):
        """Declare a variable in the current scope."""
        if name in self.scope_stack[-1]:
            self.errors.append(f"Variable '{name}' already declared in this scope")
        else:
            self.scope_stack[-1][name] = type_
    
    def _lookup_variable(self, name: str) -> Optional[HixaType]:
        """Look up a variable's type in the scope chain."""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None
    
    def _error(self, message: str):
        """Add a type error."""
        self.errors.append(message)


class TypeInferrer:
    """Type inference for Hixa expressions."""
    
    @staticmethod
    def infer_literal_type(literal) -> HixaType:
        """Infer the type of a literal value."""
        if literal.type_ == "int":
            return IntType()
        elif literal.type_ == "float":
            return FloatType()
        elif literal.type_ == "string":
            return StringType()
        elif literal.type_ == "boolean":
            return BooleanType()
        elif literal.type_ == "null":
            return VoidType()
        else:
            raise ValueError(f"Unknown literal type: {literal.type_}")
    
    @staticmethod
    def infer_binary_expression_type(left_type: HixaType, operator: str, right_type: HixaType) -> HixaType:
        """Infer the type of a binary expression."""
        # Arithmetic operators
        if operator in ['+', '-', '*', '/', '%']:
            if isinstance(left_type, IntType) and isinstance(right_type, IntType):
                return IntType()
            elif isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
                return FloatType()
            elif operator == '+' and isinstance(left_type, StringType) and isinstance(right_type, StringType):
                return StringType()
            else:
                raise TypeError(f"Cannot apply operator '{operator}' to types {left_type} and {right_type}")
        
        # Comparison operators
        elif operator in ['==', '!=', '<', '<=', '>', '>=']:
            return BooleanType()
        
        # Logical operators
        elif operator in ['&&', '||']:
            if isinstance(left_type, BooleanType) and isinstance(right_type, BooleanType):
                return BooleanType()
            else:
                raise TypeError(f"Cannot apply logical operator '{operator}' to types {left_type} and {right_type}")
        
        else:
            raise ValueError(f"Unknown binary operator: {operator}")
    
    @staticmethod
    def infer_unary_expression_type(operator: str, operand_type: HixaType) -> HixaType:
        """Infer the type of a unary expression."""
        if operator == '!':
            if isinstance(operand_type, BooleanType):
                return BooleanType()
            else:
                raise TypeError(f"Cannot apply logical NOT to type {operand_type}")
        elif operator == '-':
            if isinstance(operand_type, (IntType, FloatType)):
                return operand_type
            else:
                raise TypeError(f"Cannot apply unary minus to type {operand_type}")
        else:
            raise ValueError(f"Unknown unary operator: {operator}")


# Type system constants
INT_TYPE = IntType()
FLOAT_TYPE = FloatType()
STRING_TYPE = StringType()
BOOLEAN_TYPE = BooleanType()
VOID_TYPE = VoidType() 