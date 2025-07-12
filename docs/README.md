# Hixa Programming Language Documentation

## Overview

Hixa is a modern, production-ready programming language implemented in Python. It features a clean syntax, static typing, and a rich standard library.

## Language Features

### Basic Syntax

Hixa uses a C-like syntax with modern conveniences:

```hixa
// This is a comment
let x = 42;                    // Variable declaration
let name = "Hixa";             // String literal
let is_active = true;          // Boolean literal
```

### Variables and Types

Hixa supports several basic types:

- **Integers**: `42`, `-10`, `0`
- **Floats**: `3.14`, `-2.5`, `0.0`
- **Strings**: `"Hello, World!"`
- **Booleans**: `true`, `false`
- **Arrays**: `[1, 2, 3, 4, 5]`
- **Objects**: `{ name: "John", age: 30 }`

### Functions

Functions are declared using the `fn` keyword:

```hixa
fn add(a: int, b: int) -> int {
    return a + b;
}

fn greet(name: str) {
    print("Hello, {name}!");
}
```

### Control Flow

#### If Statements

```hixa
if x > 10 {
    print("x is greater than 10");
} else if x == 10 {
    print("x is exactly 10");
} else {
    print("x is less than 10");
}
```

#### Loops

```hixa
// While loop
while condition {
    // loop body
}

// For loop
for i in range(10) {
    print(i);
}
```

### Arrays

Arrays are zero-indexed and support various operations:

```hixa
let numbers = [1, 2, 3, 4, 5];
let first = numbers[0];        // Access element
numbers[1] = 10;               // Modify element
let length = len(numbers);     // Get length
```

### Objects

Objects are collections of key-value pairs:

```hixa
let person = {
    name: "Alice",
    age: 30,
    city: "New York"
};

let name = person.name;        // Access property
person.age = 31;               // Modify property
```

## Standard Library

Hixa comes with a comprehensive standard library:

### I/O Functions

- `print(...)` - Print values to stdout
- `input(prompt)` - Read input from stdin
- `read_file(filename)` - Read file contents
- `write_file(filename, content)` - Write content to file

### Array Functions

- `len(array)` - Get array length
- `push(array, value)` - Add value to end
- `pop(array)` - Remove and return last element
- `sort(array)` - Sort array in place
- `reverse(array)` - Reverse array in place

### Math Functions

- `abs(value)` - Absolute value
- `min(...)` - Minimum value
- `max(...)` - Maximum value
- `sqrt(value)` - Square root
- `pow(base, exponent)` - Power function
- `sin(value)`, `cos(value)`, `tan(value)` - Trigonometric functions

### String Functions

- `upper(string)` - Convert to uppercase
- `lower(string)` - Convert to lowercase
- `trim(string)` - Remove whitespace
- `replace(string, old, new)` - Replace substrings
- `contains(string, substring)` - Check if contains substring

### Utility Functions

- `range(start, end, step)` - Create range of integers
- `map(func, array)` - Apply function to array elements
- `filter(func, array)` - Filter array elements
- `reduce(func, array, initial)` - Reduce array to single value

## Command Line Interface

The Hixa language provides a comprehensive CLI:

### Running Programs

```bash
hixa run program.hx
```

### Syntax Checking

```bash
hixa check program.hx
```

### REPL

```bash
hixa repl
```

### Project Initialization

```bash
hixa init
```

## Examples

### Hello World

```hixa
fn main() {
    print("Hello, Hixa!");
}

main();
```

### Fibonacci Sequence

```hixa
fn fibonacci(n: int) -> int {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fn main() {
    for i in range(10) {
        let result = fibonacci(i);
        print("fibonacci({i}) = {result}");
    }
}

main();
```

### Calculator

```hixa
fn add(a: int, b: int) -> int {
    return a + b;
}

fn subtract(a: int, b: int) -> int {
    return a - b;
}

fn multiply(a: int, b: int) -> int {
    return a * b;
}

fn divide(a: int, b: int) -> float {
    if b == 0 {
        print("Error: Division by zero!");
        return 0;
    }
    return a / b;
}

fn main() {
    let a = 10;
    let b = 3;
    
    print("Calculator Demo:");
    print("a = {a}, b = {b}");
    
    let sum = add(a, b);
    print("a + b = {sum}");
    
    let diff = subtract(a, b);
    print("a - b = {diff}");
    
    let product = multiply(a, b);
    print("a * b = {product}");
    
    let quotient = divide(a, b);
    print("a / b = {quotient}");
}

main();
```

## Error Handling

Hixa provides clear error messages for common issues:

- **Lexical errors**: Invalid characters or tokens
- **Parsing errors**: Syntax errors in the code
- **Runtime errors**: Errors during execution

## Best Practices

1. **Use meaningful variable names**
2. **Add type annotations for clarity**
3. **Use functions to organize code**
4. **Handle errors appropriately**
5. **Write clear comments**

## Future Features

- Package management system
- WebAssembly compilation
- Improved IDE support
- Concurrency primitives
- Foreign function interface
- Performance optimizations 