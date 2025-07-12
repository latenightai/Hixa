"""
Interpreter for the Hixa programming language.

This module handles the execution of Hixa programs by walking the AST
and performing the corresponding operations.
"""

from typing import Dict, List, Optional, Any, Callable
from .ast import (
    ASTVisitor, ASTNode, Identifier, MemberExpression, 
    BinaryExpression, UnaryExpression, Literal, CallExpression,
    BlockStatement, IfStatement, WhileStatement, ForStatement,
    ReturnStatement, AssignmentExpression, ArrayExpression,
    ObjectExpression, IndexExpression, Program, FunctionDeclaration,
    VariableDeclaration
)
from .types import HixaType, IntType, FloatType, StringType, BooleanType, VoidType


class Environment:
    """Represents a scope/environment for variable storage."""
    
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing
    
    def define(self, name: str, value: Any):
        """Define a variable in this environment."""
        self.values[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable value."""
        if name in self.values:
            return self.values[name]
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise RuntimeError(f"Undefined variable '{name}'")
    
    def assign(self, name: str, value: Any):
        """Assign a value to a variable."""
        if name in self.values:
            self.values[name] = value
            return
        
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeError(f"Undefined variable '{name}'")
    
    def get_at(self, distance: int, name: str) -> Any:
        """Get a variable at a specific distance in the scope chain."""
        return self.ancestor(distance).values[name]
    
    def assign_at(self, distance: int, name: str, value: Any):
        """Assign a value to a variable at a specific distance."""
        self.ancestor(distance).values[name] = value
    
    def ancestor(self, distance: int) -> 'Environment':
        """Get an ancestor environment at the specified distance."""
        environment: Environment = self
        for _ in range(distance):
            if environment.enclosing is None:
                raise RuntimeError("Invalid scope depth")
            environment = environment.enclosing
        return environment


class HixaFunction:
    """Represents a Hixa function."""
    
    def __init__(self, declaration, closure: Environment):
        self.declaration = declaration
        self.closure = closure
    
    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        """Call the function with the given arguments."""
        environment = Environment(self.closure)
        
        # Bind parameters to arguments
        for param, arg in zip(self.declaration.parameters, arguments):
            environment.define(param.name, arg)
        
        try:
            interpreter.execute_block(self.declaration.body.statements, environment)
        except Return as return_value:
            return return_value.value
        
        return None
    
    def __str__(self) -> str:
        return f"<fn {self.declaration.name}>"


class Return(Exception):
    """Exception used for return statements."""
    
    def __init__(self, value: Any):
        self.value = value


class Interpreter(ASTVisitor):
    """Interpreter for Hixa programs."""
    
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals: Dict[int, int] = {}  # Use id() of ASTNode as key
        
        # Initialize standard library
        self._init_stdlib()
    
    def _init_stdlib(self):
        """Initialize the standard library functions."""
        # English function names
        self.globals.define("print", self._print)
        self.globals.define("len", self._len)
        self.globals.define("range", self._range)
        self.globals.define("input", self._input)
        self.globals.define("int", self._int)
        self.globals.define("float", self._float)
        self.globals.define("string", self._string)
        self.globals.define("bool", self._bool)
        
        # Assamese function names
        self.globals.define("print_kora", self._print)
        self.globals.define("likha", self._print)
        self.globals.define("length_kora", self._len)
        self.globals.define("input_lou", self._input)
        self.globals.define("random_kora", self._random)
        self.globals.define("time_kora", self._time)
        self.globals.define("sleep_kora", self._sleep)
        self.globals.define("clear_kora", self._clear)
        self.globals.define("add_kora", self._append)
        self.globals.define("remove_kora", self._remove)
        self.globals.define("sort_kora", self._sort)
        self.globals.define("reverse_kora", self._reverse)
        self.globals.define("bisora", self._find)
        self.globals.define("replace_kora", self._replace)
        self.globals.define("split_kora", self._split)
        self.globals.define("join_kora", self._join)
        self.globals.define("upper_kora", self._upper)
        self.globals.define("lower_kora", self._lower)
        self.globals.define("round_kora", self._round)
        self.globals.define("floor_kora", self._floor)
        self.globals.define("ceil_kora", self._ceil)
        self.globals.define("abs_kora", self._abs)
        self.globals.define("sqrt_kora", self._sqrt)
        self.globals.define("pow_kora", self._pow)
        self.globals.define("sin_kora", self._sin)
        self.globals.define("cos_kora", self._cos)
        self.globals.define("tan_kora", self._tan)
        self.globals.define("log_kora", self._log)
        self.globals.define("exp_kora", self._exp)
        self.globals.define("min_kora", self._min)
        self.globals.define("max_kora", self._max)
        self.globals.define("sum_kora", self._sum)
        self.globals.define("average_kora", self._average)
        self.globals.define("count_kora", self._count)
        self.globals.define("copy_kora", self._copy)
        self.globals.define("delete_kora", self._delete)
        self.globals.define("check_kora", self._check)
        self.globals.define("convert_kora", self._convert)
        self.globals.define("format_kora", self._format)
        self.globals.define("validate_kora", self._validate)
        self.globals.define("error_kora", self._error)
    
    def interpret(self, statements: List[ASTNode]):
        """Interpret a list of statements."""
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            raise error
    
    def execute(self, statement: ASTNode):
        """Execute a single statement."""
        statement.accept(self)
    
    def evaluate(self, expression: ASTNode) -> Any:
        """Evaluate an expression."""
        return expression.accept(self)
    
    def execute_block(self, statements: List[ASTNode], environment: Environment):
        """Execute a block of statements in a given environment."""
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    
    def resolve(self, expr: ASTNode, depth: int):
        """Resolve a variable to its scope depth."""
        self.locals[id(expr)] = depth
    
    def lookup_variable(self, name: str, expr: ASTNode) -> Any:
        """Look up a variable by name and expression."""
        return self.environment.get(name)
    
    def assign_variable(self, name: str, value: Any, expr: ASTNode):
        """Assign a value to a variable."""
        self.environment.assign(name, value)
    
    # AST Visitor methods
    def visit_program(self, node):
        """Visit a program node."""
        for statement in node.statements:
            self.execute(statement)
        return None
    
    def visit_function_declaration(self, node):
        """Visit a function declaration node."""
        function = HixaFunction(node, self.environment)
        self.environment.define(node.name, function)
        return None
    
    def visit_variable_declaration(self, node):
        """Visit a variable declaration node."""
        value = None
        if node.initializer:
            value = self.evaluate(node.initializer)
        
        self.environment.define(node.name, value)
        return None
    
    def visit_binary_expression(self, node):
        """Visit a binary expression node."""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        if node.operator == "+":
            return self._add(left, right)
        elif node.operator == "-":
            return self._subtract(left, right)
        elif node.operator == "*":
            return self._multiply(left, right)
        elif node.operator == "/":
            return self._divide(left, right)
        elif node.operator == "%":
            return self._modulo(left, right)
        elif node.operator == "==":
            return self._equal(left, right)
        elif node.operator == "!=":
            return self._not_equal(left, right)
        elif node.operator == "<":
            return self._less(left, right)
        elif node.operator == "<=":
            return self._less_equal(left, right)
        elif node.operator == ">":
            return self._greater(left, right)
        elif node.operator == ">=":
            return self._greater_equal(left, right)
        elif node.operator == "&&":
            return self._and(left, right)
        elif node.operator == "||":
            return self._or(left, right)
        
        raise RuntimeError(f"Unknown binary operator: {node.operator}")
    
    def visit_unary_expression(self, node):
        """Visit a unary expression node."""
        right = self.evaluate(node.operand)
        
        if node.operator == "-":
            return self._negate(right)
        elif node.operator == "!":
            return self._not(right)
        
        raise RuntimeError(f"Unknown unary operator: {node.operator}")
    
    def visit_literal(self, node):
        """Visit a literal node."""
        return node.value
    
    def visit_identifier(self, node):
        """Visit an identifier node."""
        return self.lookup_variable(node.name, node)
    
    def visit_call_expression(self, node):
        """Visit a call expression node."""
        callee = self.evaluate(node.callee)
        
        arguments = []
        for argument in node.arguments:
            arguments.append(self.evaluate(argument))
        
        # If it's a HixaFunction, check argument count
        if hasattr(callee, 'declaration'):
            if len(arguments) != len(callee.declaration.parameters):
                raise RuntimeError(f"Expected {len(callee.declaration.parameters)} arguments but got {len(arguments)}")
            return callee.call(self, arguments)
        # If it's a native Python callable (standard library)
        elif callable(callee):
            return callee(*arguments)
        else:
            raise RuntimeError("Can only call functions")
    
    def visit_block_statement(self, node):
        """Visit a block statement node."""
        self.execute_block(node.statements, Environment(self.environment))
        return None
    
    def visit_if_statement(self, node):
        """Visit an if statement node."""
        if self._is_truthy(self.evaluate(node.condition)):
            self.execute(node.then_branch)
        elif node.else_branch:
            self.execute(node.else_branch)
        return None
    
    def visit_while_statement(self, node):
        """Visit a while statement node."""
        while self._is_truthy(self.evaluate(node.condition)):
            self.execute(node.body)
        return None
    
    def visit_for_statement(self, node):
        """Visit a for statement node."""
        if node.initializer:
            self.execute(node.initializer)
        
        while True:
            if node.condition:
                if not self._is_truthy(self.evaluate(node.condition)):
                    break
            
            self.execute(node.body)
            
            if node.increment:
                self.evaluate(node.increment)
        
        return None
    
    def visit_return_statement(self, node):
        """Visit a return statement node."""
        value = None
        if node.value:
            value = self.evaluate(node.value)
        
        raise Return(value)
    
    def visit_assignment_expression(self, node):
        """Visit an assignment expression node."""
        value = self.evaluate(node.value)
        
        if isinstance(node.target, Identifier):
            self.assign_variable(node.target.name, value, node.target)
        elif isinstance(node.target, MemberExpression):
            object_ = self.evaluate(node.target.object_)
            if isinstance(node.target.property, Identifier):
                setattr(object_, node.target.property.name, value)
            else:
                raise RuntimeError("Only identifiers can be used as object properties")
        else:
            raise RuntimeError("Invalid assignment target")
        
        return value
    
    def visit_member_expression(self, node):
        """Visit a member expression node."""
        object_ = self.evaluate(node.object_)
        
        if isinstance(node.property, Identifier):
            return getattr(object_, node.property.name)
        else:
            raise RuntimeError("Only identifiers can be used as object properties")
    
    def visit_array_expression(self, node):
        """Visit an array expression node."""
        elements = []
        for element in node.elements:
            elements.append(self.evaluate(element))
        return elements
    
    def visit_object_expression(self, node):
        """Visit an object expression node."""
        obj = {}
        for property_ in node.properties:
            obj[property_.key] = self.evaluate(property_.value)
        return obj
    
    def visit_index_expression(self, node):
        """Visit an index expression node."""
        array = self.evaluate(node.array)
        index = self.evaluate(node.index)
        
        if not isinstance(array, list):
            raise RuntimeError("Only arrays can be indexed")
        
        if not isinstance(index, int):
            raise RuntimeError("Array index must be an integer")
        
        if index < 0 or index >= len(array):
            raise RuntimeError("Array index out of bounds")
        
        return array[index]
    
    # Helper methods for operations
    def _is_truthy(self, value: Any) -> bool:
        """Check if a value is truthy."""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True
    
    def _add(self, left: Any, right: Any) -> Any:
        """Add two values."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        elif isinstance(left, str) and isinstance(right, str):
            return left + right
        else:
            raise RuntimeError("Operands must be two numbers or two strings")
    
    def _subtract(self, left: Any, right: Any) -> Any:
        """Subtract two values."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _multiply(self, left: Any, right: Any) -> Any:
        """Multiply two values."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _divide(self, left: Any, right: Any) -> Any:
        """Divide two values."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _modulo(self, left: Any, right: Any) -> Any:
        """Modulo two values."""
        if isinstance(left, int) and isinstance(right, int):
            if right == 0:
                raise RuntimeError("Modulo by zero")
            return left % right
        else:
            raise RuntimeError("Operands must be integers")
    
    def _equal(self, left: Any, right: Any) -> bool:
        """Check if two values are equal."""
        return left == right
    
    def _not_equal(self, left: Any, right: Any) -> bool:
        """Check if two values are not equal."""
        return left != right
    
    def _less(self, left: Any, right: Any) -> bool:
        """Check if left is less than right."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left < right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _less_equal(self, left: Any, right: Any) -> bool:
        """Check if left is less than or equal to right."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left <= right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _greater(self, left: Any, right: Any) -> bool:
        """Check if left is greater than right."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left > right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _greater_equal(self, left: Any, right: Any) -> bool:
        """Check if left is greater than or equal to right."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left >= right
        else:
            raise RuntimeError("Operands must be numbers")
    
    def _and(self, left: Any, right: Any) -> bool:
        """Logical AND."""
        return self._is_truthy(left) and self._is_truthy(right)
    
    def _or(self, left: Any, right: Any) -> bool:
        """Logical OR."""
        return self._is_truthy(left) or self._is_truthy(right)
    
    def _negate(self, value: Any) -> Any:
        """Negate a value."""
        if isinstance(value, (int, float)):
            return -value
        else:
            raise RuntimeError("Operand must be a number")
    
    def _not(self, value: Any) -> bool:
        """Logical NOT."""
        return not self._is_truthy(value)
    
    # Standard library functions
    def _print(self, *args):
        """Print function."""
        print(*args)
        return None
    
    def _len(self, value):
        """Length function."""
        if isinstance(value, (str, list)):
            return len(value)
        else:
            raise RuntimeError("len() can only be called on strings and arrays")
    
    def _range(self, end):
        """Range function."""
        if isinstance(end, int):
            return list(range(end))
        else:
            raise RuntimeError("range() argument must be an integer")
    
    def _input(self, prompt=""):
        """Input function."""
        return input(prompt)
    
    def _int(self, value):
        """Convert to integer."""
        try:
            return int(value)
        except (ValueError, TypeError):
            raise RuntimeError("Cannot convert to integer")
    
    def _float(self, value):
        """Convert to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            raise RuntimeError("Cannot convert to float")
    
    def _string(self, value):
        """Convert to string."""
        return str(value)
    
    def _bool(self, value):
        """Convert to boolean."""
        return self._is_truthy(value)
    
    # Additional standard library functions for Assamese keywords
    def _random(self, max_val=100):
        """Generate random number."""
        import random
        return random.randint(0, max_val)
    
    def _time(self):
        """Get current time."""
        import time
        return time.time()
    
    def _sleep(self, seconds):
        """Sleep for given seconds."""
        import time
        time.sleep(seconds)
        return None
    
    def _clear(self):
        """Clear screen."""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
        return None
    
    def _append(self, list_obj, item):
        """Append item to list."""
        if isinstance(list_obj, list):
            list_obj.append(item)
            return list_obj
        else:
            raise RuntimeError("append() can only be called on lists")
    
    def _remove(self, list_obj, item):
        """Remove item from list."""
        if isinstance(list_obj, list):
            if item in list_obj:
                list_obj.remove(item)
            return list_obj
        else:
            raise RuntimeError("remove() can only be called on lists")
    
    def _sort(self, list_obj):
        """Sort list."""
        if isinstance(list_obj, list):
            list_obj.sort()
            return list_obj
        else:
            raise RuntimeError("sort() can only be called on lists")
    
    def _reverse(self, list_obj):
        """Reverse list."""
        if isinstance(list_obj, list):
            list_obj.reverse()
            return list_obj
        else:
            raise RuntimeError("reverse() can only be called on lists")
    
    def _find(self, container, item):
        """Find item in string or list."""
        if isinstance(container, str):
            return container.find(item)
        elif isinstance(container, list):
            try:
                return container.index(item)
            except ValueError:
                return -1
        else:
            raise RuntimeError("find() can only be called on strings and lists")
    
    def _replace(self, string, old, new):
        """Replace in string."""
        if isinstance(string, str):
            return string.replace(old, new)
        else:
            raise RuntimeError("replace() can only be called on strings")
    
    def _split(self, string, delimiter=" "):
        """Split string."""
        if isinstance(string, str):
            return string.split(delimiter)
        else:
            raise RuntimeError("split() can only be called on strings")
    
    def _join(self, list_obj, separator=""):
        """Join list into string."""
        if isinstance(list_obj, list):
            return separator.join(str(item) for item in list_obj)
        else:
            raise RuntimeError("join() can only be called on lists")
    
    def _upper(self, string):
        """Convert to uppercase."""
        if isinstance(string, str):
            return string.upper()
        else:
            raise RuntimeError("upper() can only be called on strings")
    
    def _lower(self, string):
        """Convert to lowercase."""
        if isinstance(string, str):
            return string.lower()
        else:
            raise RuntimeError("lower() can only be called on strings")
    
    def _round(self, number, decimals=0):
        """Round number."""
        if isinstance(number, (int, float)):
            return round(number, decimals)
        else:
            raise RuntimeError("round() can only be called on numbers")
    
    def _floor(self, number):
        """Floor of number."""
        import math
        if isinstance(number, (int, float)):
            return math.floor(number)
        else:
            raise RuntimeError("floor() can only be called on numbers")
    
    def _ceil(self, number):
        """Ceiling of number."""
        import math
        if isinstance(number, (int, float)):
            return math.ceil(number)
        else:
            raise RuntimeError("ceil() can only be called on numbers")
    
    def _abs(self, number):
        """Absolute value."""
        if isinstance(number, (int, float)):
            return abs(number)
        else:
            raise RuntimeError("abs() can only be called on numbers")
    
    def _sqrt(self, number):
        """Square root."""
        import math
        if isinstance(number, (int, float)):
            if number < 0:
                raise RuntimeError("Cannot take square root of negative number")
            return math.sqrt(number)
        else:
            raise RuntimeError("sqrt() can only be called on numbers")
    
    def _pow(self, base, exponent):
        """Power function."""
        import math
        if isinstance(base, (int, float)) and isinstance(exponent, (int, float)):
            return math.pow(base, exponent)
        else:
            raise RuntimeError("pow() arguments must be numbers")
    
    def _sin(self, angle):
        """Sine function."""
        import math
        if isinstance(angle, (int, float)):
            return math.sin(angle)
        else:
            raise RuntimeError("sin() can only be called on numbers")
    
    def _cos(self, angle):
        """Cosine function."""
        import math
        if isinstance(angle, (int, float)):
            return math.cos(angle)
        else:
            raise RuntimeError("cos() can only be called on numbers")
    
    def _tan(self, angle):
        """Tangent function."""
        import math
        if isinstance(angle, (int, float)):
            return math.tan(angle)
        else:
            raise RuntimeError("tan() can only be called on numbers")
    
    def _log(self, number, base=10):
        """Logarithm function."""
        import math
        if isinstance(number, (int, float)) and isinstance(base, (int, float)):
            if number <= 0 or base <= 0:
                raise RuntimeError("Logarithm arguments must be positive")
            return math.log(number, base)
        else:
            raise RuntimeError("log() arguments must be numbers")
    
    def _exp(self, number):
        """Exponential function."""
        import math
        if isinstance(number, (int, float)):
            return math.exp(number)
        else:
            raise RuntimeError("exp() can only be called on numbers")
    
    def _min(self, *args):
        """Minimum value."""
        if len(args) == 1 and isinstance(args[0], list):
            return min(args[0])
        elif all(isinstance(arg, (int, float)) for arg in args):
            return min(args)
        else:
            raise RuntimeError("min() arguments must be numbers or a list")
    
    def _max(self, *args):
        """Maximum value."""
        if len(args) == 1 and isinstance(args[0], list):
            return max(args[0])
        elif all(isinstance(arg, (int, float)) for arg in args):
            return max(args)
        else:
            raise RuntimeError("max() arguments must be numbers or a list")
    
    def _sum(self, list_obj):
        """Sum of list."""
        if isinstance(list_obj, list):
            if all(isinstance(item, (int, float)) for item in list_obj):
                return sum(list_obj)
            else:
                raise RuntimeError("sum() list must contain only numbers")
        else:
            raise RuntimeError("sum() can only be called on lists")
    
    def _average(self, list_obj):
        """Average of list."""
        if isinstance(list_obj, list) and len(list_obj) > 0:
            if all(isinstance(item, (int, float)) for item in list_obj):
                return sum(list_obj) / len(list_obj)
            else:
                raise RuntimeError("average() list must contain only numbers")
        else:
            raise RuntimeError("average() can only be called on non-empty lists")
    
    def _count(self, container, item):
        """Count occurrences."""
        if isinstance(container, (str, list)):
            return container.count(item)
        else:
            raise RuntimeError("count() can only be called on strings and lists")
    
    def _copy(self, obj):
        """Copy object."""
        import copy
        return copy.deepcopy(obj)
    
    def _delete(self, name):
        """Delete variable."""
        if name in self.environment.values:
            del self.environment.values[name]
            return True
        else:
            return False
    
    def _check(self, name):
        """Check if variable exists."""
        return name in self.environment.values
    
    def _convert(self, value, target_type):
        """Convert type."""
        if target_type == "int":
            return self._int(value)
        elif target_type == "float":
            return self._float(value)
        elif target_type == "string":
            return self._string(value)
        elif target_type == "bool":
            return self._bool(value)
        else:
            raise RuntimeError(f"Unknown type: {target_type}")
    
    def _format(self, template, *args):
        """Format string."""
        if isinstance(template, str):
            return template.format(*args)
        else:
            raise RuntimeError("format() template must be a string")
    
    def _validate(self, value, condition):
        """Validate input."""
        # Simple validation - can be extended
        if condition == "positive" and isinstance(value, (int, float)):
            return value > 0
        elif condition == "negative" and isinstance(value, (int, float)):
            return value < 0
        elif condition == "nonempty" and isinstance(value, str):
            return len(value) > 0
        else:
            return True
    
    def _error(self, message):
        """Handle error."""
        raise RuntimeError(message) 