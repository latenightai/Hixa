"""
Standard library for the Hixa programming language.

This module provides built-in functions and utilities that are
available to all Hixa programs.
"""

from typing import Any, List, Dict, Callable, Optional, Union
import math
import random
import time


class StandardLibrary:
    """Standard library functions for Hixa."""
    
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self._init_functions()
    
    def _init_functions(self):
        """Initialize all standard library functions."""
        # I/O functions
        self.functions.update({
            'print': self._print,
            'input': self._input,
            'read_file': self._read_file,
            'write_file': self._write_file,
        })
        
        # Type conversion functions
        self.functions.update({
            'int': self._int,
            'float': self._float,
            'string': self._string,
            'bool': self._bool,
            'array': self._array,
        })
        
        # Array functions
        self.functions.update({
            'len': self._len,
            'push': self._push,
            'pop': self._pop,
            'insert': self._insert,
            'remove': self._remove,
            'sort': self._sort,
            'reverse': self._reverse,
            'join': self._join,
            'split': self._split,
        })
        
        # Math functions
        self.functions.update({
            'abs': self._abs,
            'min': self._min,
            'max': self._max,
            'sqrt': self._sqrt,
            'pow': self._pow,
            'floor': self._floor,
            'ceil': self._ceil,
            'round': self._round,
            'sin': self._sin,
            'cos': self._cos,
            'tan': self._tan,
            'log': self._log,
            'exp': self._exp,
        })
        
        # Random functions
        self.functions.update({
            'random': self._random,
            'randint': self._randint,
            'choice': self._choice,
            'shuffle': self._shuffle,
        })
        
        # Time functions
        self.functions.update({
            'time': self._time,
            'sleep': self._sleep,
        })
        
        # String functions
        self.functions.update({
            'upper': self._upper,
            'lower': self._lower,
            'trim': self._trim,
            'replace': self._replace,
            'contains': self._contains,
            'starts_with': self._starts_with,
            'ends_with': self._ends_with,
            'substring': self._substring,
        })
        
        # Utility functions
        self.functions.update({
            'range': self._range,
            'map': self._map,
            'filter': self._filter,
            'reduce': self._reduce,
            'zip': self._zip,
            'enumerate': self._enumerate,
        })
    
    # I/O functions
    def _print(self, *args):
        """Print values to stdout."""
        print(*args)
        return None
    
    def _input(self, prompt=""):
        """Read input from stdin."""
        return input(prompt)
    
    def _read_file(self, filename: str) -> str:
        """Read contents of a file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Error reading file '{filename}': {e}")
    
    def _write_file(self, filename: str, content: str):
        """Write content to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return None
        except Exception as e:
            raise RuntimeError(f"Error writing file '{filename}': {e}")
    
    # Type conversion functions
    def _int(self, value) -> int:
        """Convert value to integer."""
        try:
            return int(value)
        except (ValueError, TypeError):
            raise RuntimeError(f"Cannot convert '{value}' to integer")
    
    def _float(self, value) -> float:
        """Convert value to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            raise RuntimeError(f"Cannot convert '{value}' to float")
    
    def _string(self, value) -> str:
        """Convert value to string."""
        return str(value)
    
    def _bool(self, value) -> bool:
        """Convert value to boolean."""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value != ""
        if isinstance(value, list):
            return len(value) > 0
        return True
    
    def _array(self, *args) -> List:
        """Create an array from arguments."""
        return list(args)
    
    # Array functions
    def _len(self, value) -> int:
        """Get length of string, array, or object."""
        if isinstance(value, (str, list, dict)):
            return len(value)
        else:
            raise RuntimeError("len() can only be called on strings, arrays, and objects")
    
    def _push(self, array: List, value: Any) -> int:
        """Add value to end of array and return new length."""
        if not isinstance(array, list):
            raise RuntimeError("push() can only be called on arrays")
        array.append(value)
        return len(array)
    
    def _pop(self, array: List) -> Any:
        """Remove and return last element of array."""
        if not isinstance(array, list):
            raise RuntimeError("pop() can only be called on arrays")
        if len(array) == 0:
            raise RuntimeError("Cannot pop from empty array")
        return array.pop()
    
    def _insert(self, array: List, index: int, value: Any):
        """Insert value at index in array."""
        if not isinstance(array, list):
            raise RuntimeError("insert() can only be called on arrays")
        if index < 0 or index > len(array):
            raise RuntimeError("Index out of bounds")
        array.insert(index, value)
        return None
    
    def _remove(self, array: List, value: Any) -> bool:
        """Remove first occurrence of value from array."""
        if not isinstance(array, list):
            raise RuntimeError("remove() can only be called on arrays")
        try:
            array.remove(value)
            return True
        except ValueError:
            return False
    
    def _sort(self, array: List, reverse: bool = False) -> List:
        """Sort array in place and return sorted array."""
        if not isinstance(array, list):
            raise RuntimeError("sort() can only be called on arrays")
        array.sort(reverse=reverse)
        return array
    
    def _reverse(self, array: List) -> List:
        """Reverse array in place and return reversed array."""
        if not isinstance(array, list):
            raise RuntimeError("reverse() can only be called on arrays")
        array.reverse()
        return array
    
    def _join(self, array: List, separator: str = "") -> str:
        """Join array elements into a string."""
        if not isinstance(array, list):
            raise RuntimeError("join() can only be called on arrays")
        return separator.join(str(item) for item in array)
    
    def _split(self, string: str, separator: Optional[str] = None) -> List[str]:
        """Split string into array."""
        if not isinstance(string, str):
            raise RuntimeError("split() can only be called on strings")
        if separator is None:
            return string.split()
        return string.split(separator)
    
    # Math functions
    def _abs(self, value) -> float:
        """Get absolute value."""
        if isinstance(value, (int, float)):
            return abs(value)
        else:
            raise RuntimeError("abs() can only be called on numbers")
    
    def _min(self, *args) -> Any:
        """Get minimum value."""
        if len(args) == 0:
            raise RuntimeError("min() requires at least one argument")
        return min(args)
    
    def _max(self, *args) -> Any:
        """Get maximum value."""
        if len(args) == 0:
            raise RuntimeError("max() requires at least one argument")
        return max(args)
    
    def _sqrt(self, value) -> float:
        """Get square root."""
        if isinstance(value, (int, float)):
            if value < 0:
                raise RuntimeError("Cannot take square root of negative number")
            return math.sqrt(value)
        else:
            raise RuntimeError("sqrt() can only be called on numbers")
    
    def _pow(self, base, exponent) -> float:
        """Raise base to the power of exponent."""
        if isinstance(base, (int, float)) and isinstance(exponent, (int, float)):
            return math.pow(base, exponent)
        else:
            raise RuntimeError("pow() arguments must be numbers")
    
    def _floor(self, value) -> int:
        """Get floor of value."""
        if isinstance(value, (int, float)):
            return math.floor(value)
        else:
            raise RuntimeError("floor() can only be called on numbers")
    
    def _ceil(self, value) -> int:
        """Get ceiling of value."""
        if isinstance(value, (int, float)):
            return math.ceil(value)
        else:
            raise RuntimeError("ceil() can only be called on numbers")
    
    def _round(self, value, digits: int = 0) -> float:
        """Round value to specified number of digits."""
        if isinstance(value, (int, float)):
            return round(value, digits)
        else:
            raise RuntimeError("round() can only be called on numbers")
    
    def _sin(self, value) -> float:
        """Get sine of value (in radians)."""
        if isinstance(value, (int, float)):
            return math.sin(value)
        else:
            raise RuntimeError("sin() can only be called on numbers")
    
    def _cos(self, value) -> float:
        """Get cosine of value (in radians)."""
        if isinstance(value, (int, float)):
            return math.cos(value)
        else:
            raise RuntimeError("cos() can only be called on numbers")
    
    def _tan(self, value) -> float:
        """Get tangent of value (in radians)."""
        if isinstance(value, (int, float)):
            return math.tan(value)
        else:
            raise RuntimeError("tan() can only be called on numbers")
    
    def _log(self, value, base: float = math.e) -> float:
        """Get logarithm of value with given base."""
        if isinstance(value, (int, float)):
            if value <= 0:
                raise RuntimeError("Cannot take logarithm of non-positive number")
            return math.log(value, base)
        else:
            raise RuntimeError("log() can only be called on numbers")
    
    def _exp(self, value) -> float:
        """Get e raised to the power of value."""
        if isinstance(value, (int, float)):
            return math.exp(value)
        else:
            raise RuntimeError("exp() can only be called on numbers")
    
    # Random functions
    def _random(self) -> float:
        """Get random float between 0 and 1."""
        return random.random()
    
    def _randint(self, start: int, end: int) -> int:
        """Get random integer between start and end (inclusive)."""
        if isinstance(start, int) and isinstance(end, int):
            return random.randint(start, end)
        else:
            raise RuntimeError("randint() arguments must be integers")
    
    def _choice(self, array: List) -> Any:
        """Get random element from array."""
        if not isinstance(array, list):
            raise RuntimeError("choice() can only be called on arrays")
        if len(array) == 0:
            raise RuntimeError("Cannot choose from empty array")
        return random.choice(array)
    
    def _shuffle(self, array: List) -> List:
        """Shuffle array in place and return shuffled array."""
        if not isinstance(array, list):
            raise RuntimeError("shuffle() can only be called on arrays")
        random.shuffle(array)
        return array
    
    # Time functions
    def _time(self) -> float:
        """Get current time in seconds since epoch."""
        return time.time()
    
    def _sleep(self, seconds: float):
        """Sleep for specified number of seconds."""
        if isinstance(seconds, (int, float)):
            time.sleep(seconds)
            return None
        else:
            raise RuntimeError("sleep() argument must be a number")
    
    # String functions
    def _upper(self, string: str) -> str:
        """Convert string to uppercase."""
        if not isinstance(string, str):
            raise RuntimeError("upper() can only be called on strings")
        return string.upper()
    
    def _lower(self, string: str) -> str:
        """Convert string to lowercase."""
        if not isinstance(string, str):
            raise RuntimeError("lower() can only be called on strings")
        return string.lower()
    
    def _trim(self, string: str) -> str:
        """Remove whitespace from beginning and end of string."""
        if not isinstance(string, str):
            raise RuntimeError("trim() can only be called on strings")
        return string.strip()
    
    def _replace(self, string: str, old: str, new: str) -> str:
        """Replace all occurrences of old with new in string."""
        if not isinstance(string, str):
            raise RuntimeError("replace() can only be called on strings")
        return string.replace(old, new)
    
    def _contains(self, string: str, substring: str) -> bool:
        """Check if string contains substring."""
        if not isinstance(string, str):
            raise RuntimeError("contains() can only be called on strings")
        return substring in string
    
    def _starts_with(self, string: str, prefix: str) -> bool:
        """Check if string starts with prefix."""
        if not isinstance(string, str):
            raise RuntimeError("starts_with() can only be called on strings")
        return string.startswith(prefix)
    
    def _ends_with(self, string: str, suffix: str) -> bool:
        """Check if string ends with suffix."""
        if not isinstance(string, str):
            raise RuntimeError("ends_with() can only be called on strings")
        return string.endswith(suffix)
    
    def _substring(self, string: str, start: int, end: Optional[int] = None) -> str:
        """Get substring of string from start to end."""
        if not isinstance(string, str):
            raise RuntimeError("substring() can only be called on strings")
        if end is None:
            end = len(string)
        return string[start:end]
    
    # Utility functions
    def _range(self, start: int, end: Optional[int] = None, step: int = 1) -> List[int]:
        """Create range of integers."""
        if end is None:
            end = start
            start = 0
        if isinstance(start, int) and isinstance(end, int) and isinstance(step, int):
            return list(range(start, end, step))
        else:
            raise RuntimeError("range() arguments must be integers")
    
    def _map(self, func, array: List) -> List:
        """Apply function to each element of array."""
        if not isinstance(array, list):
            raise RuntimeError("map() can only be called on arrays")
        if not callable(func):
            raise RuntimeError("map() first argument must be callable")
        return [func(item) for item in array]
    
    def _filter(self, func, array: List) -> List:
        """Filter array elements using function."""
        if not isinstance(array, list):
            raise RuntimeError("filter() can only be called on arrays")
        if not callable(func):
            raise RuntimeError("filter() first argument must be callable")
        return [item for item in array if func(item)]
    
    def _reduce(self, func, array: List, initial=None) -> Any:
        """Reduce array to single value using function."""
        if not isinstance(array, list):
            raise RuntimeError("reduce() can only be called on arrays")
        if not callable(func):
            raise RuntimeError("reduce() first argument must be callable")
        if len(array) == 0:
            return initial
        if initial is None:
            result = array[0]
            array = array[1:]
        else:
            result = initial
        for item in array:
            result = func(result, item)
        return result
    
    def _zip(self, *arrays) -> List[tuple]:
        """Zip multiple arrays together."""
        for array in arrays:
            if not isinstance(array, list):
                raise RuntimeError("zip() arguments must be arrays")
        return list(zip(*arrays))
    
    def _enumerate(self, array: List, start: int = 0) -> List[tuple]:
        """Enumerate array elements with indices."""
        if not isinstance(array, list):
            raise RuntimeError("enumerate() can only be called on arrays")
        return list(enumerate(array, start))
    
    def get_function(self, name: str) -> Callable:
        """Get a function by name."""
        if name not in self.functions:
            raise RuntimeError(f"Unknown function '{name}'")
        return self.functions[name]
    
    def has_function(self, name: str) -> bool:
        """Check if a function exists."""
        return name in self.functions 