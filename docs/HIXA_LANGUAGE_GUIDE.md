# Hixa Programming Language Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Syntax](#basic-syntax)
4. [Data Types](#data-types)
5. [Variables](#variables)
6. [Functions](#functions)
7. [Control Flow](#control-flow)
8. [Operators](#operators)
9. [Standard Library](#standard-library)
10. [Examples](#examples)
11. [Best Practices](#best-practices)

## Introduction

Hixa is a modern, educational programming language that supports both English and Assamese keywords. It's designed to be easy to learn while providing powerful features for programming education and development.

### Key Features
- **Bilingual Support**: Use English or Assamese keywords
- **Simple Syntax**: C-like syntax with modern conveniences
- **Rich Standard Library**: Built-in functions for common operations
- **Educational Focus**: Designed for learning programming concepts
- **Cross-platform**: Runs on any system with Python 3.8+

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install Hixa
```bash
# Clone the repository
git clone https://github.com/hixa-lang/hixa.git
cd hixa

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Verify Installation
```bash
hixa --version
```

## Basic Syntax

### File Extension
Hixa programs use the `.hx` file extension.

### Comments
```hixa
// Single-line comment
/* Multi-line comment
   spanning multiple lines */
```

### Program Structure
Every Hixa program consists of statements and declarations. The main entry point is typically a `main()` function.

```hixa
fn main() {
    print("Hello, World!");
}
```

## Data Types

Hixa supports the following basic data types:

### Numbers
```hixa
dhora integer = 42;           // Integer
dhora float = 3.14;          // Floating-point
dhora negative = -10;        // Negative numbers
```

### Strings
```hixa
dhora message = "Hello, World!";
dhora single_quote = 'Single quotes work too';
dhora multiline = "This is a
multiline string";
```

### Booleans
```hixa
dhora is_true = hosa;        // true (Assamese)
dhora is_false = misa;       // false (Assamese)
dhora is_null = nai;         // null (Assamese)

// English equivalents
dhora english_true = true;
dhora english_false = false;
dhora english_null = null;
```

### Arrays (Lists)
```hixa
dhora numbers = [1, 2, 3, 4, 5];
dhora mixed = [1, "hello", true, 3.14];
dhora empty = [];
```

## Variables

### Variable Declaration
Use `dhora` (Assamese) or `let` (English) to declare variables:

```hixa
dhora name = "John";         // Assamese keyword
let age = 25;               // English keyword
dhora is_student = hosa;
```

### Variable Assignment
```hixa
dhora x = 10;
x = 20;                     // Reassign value
x = x + 5;                  // Arithmetic assignment
```

### Variable Scope
Variables are block-scoped and follow lexical scoping rules:

```hixa
dhora global_var = "I'm global";

fn test_function() {
    dhora local_var = "I'm local";
    print(global_var);      // Can access global
    print(local_var);       // Can access local
}

// print(local_var);        // Error: local_var not in scope
```

## Functions

### Function Declaration
Use `kam` (Assamese) or `fn` (English) to declare functions:

```hixa
kam add_kora(x, y) {
    ghurai_diya (x + y);
}

fn multiply(a, b) {
    return (a * b);
}
```

### Function Parameters
Functions can take multiple parameters:

```hixa
kam greet_kora(name, age) {
    print_kora("Hello, ");
    print_kora(name);
    print_kora("! You are ");
    print_kora(age);
    print_kora(" years old.");
}
```

### Return Values
Use `ghurai_diya` (Assamese) or `return` (English) to return values:

```hixa
kam calculate_kora(x, y, operation) {
    jodi (operation == "add") {
        ghurai_diya (x + y);
    } nohole jodi (operation == "subtract") {
        ghurai_diya (x - y);
    } nohole {
        ghurai_diya 0;
    }
}
```

### Function Calls
```hixa
dhora result = add_kora(10, 20);
print_kora(result);

greet_kora("Alice", 30);
```

## Control Flow

### If Statements
```hixa
jodi (condition) {
    // code to execute if condition is true
} nohole {
    // code to execute if condition is false
}
```

### If-Else If Chains
```hixa
jodi (score >= 90) {
    print_kora("Grade: A");
} nohole jodi (score >= 80) {
    print_kora("Grade: B");
} nohole jodi (score >= 70) {
    print_kora("Grade: C");
} nohole {
    print_kora("Grade: F");
}
```

### While Loops
```hixa
jetialoike (condition); {
    // code to execute while condition is true
}
```

### For Loops
```hixa
karone (dhora i = 0; i < 10; i = i + 1) {
    print_kora(i);
}
```

### Break and Continue
```hixa
jetialoike (true); {
    jodi (condition) {
        break_kora;         // Exit the loop
    }
    jodi (skip_condition) {
        continue_kora;      // Skip to next iteration
    }
}
```

## Operators

### Arithmetic Operators
```hixa
dhora a = 10;
dhora b = 3;

dhora sum = a + b;          // Addition: 13
dhora diff = a - b;         // Subtraction: 7
dhora product = a * b;      // Multiplication: 30
dhora quotient = a / b;     // Division: 3.333...
dhora remainder = a % b;    // Modulo: 1
```

### Comparison Operators
```hixa
dhora x = 5;
dhora y = 10;

dhora equal = (x == y);     // Equal: false
dhora not_equal = (x != y); // Not equal: true
dhora less = (x < y);       // Less than: true
dhora less_eq = (x <= y);   // Less than or equal: true
dhora greater = (x > y);    // Greater than: false
dhora greater_eq = (x >= y); // Greater than or equal: false
```

### Logical Operators
```hixa
dhora a = hosa;             // true
dhora b = misa;             // false

dhora and_result = (a aru b);    // Logical AND: false
dhora or_result = (a ba b);      // Logical OR: true
dhora not_result = not_kora(a);  // Logical NOT: false
```

### Assignment Operators
```hixa
dhora x = 10;
x = x + 5;                  // x is now 15
x = x - 3;                  // x is now 12
x = x * 2;                  // x is now 24
x = x / 4;                  // x is now 6
```

## Standard Library

Hixa provides a rich standard library with both English and Assamese function names.

### Input/Output Functions

#### Print Functions
```hixa
print("Hello World");           // English
print_kora("Hello World");      // Assamese
likha("Hello World");           // Alternative Assamese
```

#### Input Functions
```hixa
dhora name = input("Enter your name: ");     // English
dhora age = input_lou("Enter your age: ");   // Assamese
```

### String Functions
```hixa
dhora text = "Hello World";

dhora upper_text = upper_kora(text);         // "HELLO WORLD"
dhora lower_text = lower_kora(text);         // "hello world"
dhora length = length_kora(text);            // 11
dhora replaced = replace_kora(text, "World", "Hixa"); // "Hello Hixa"
dhora parts = split_kora(text, " ");         // ["Hello", "World"]
dhora joined = join_kora(parts, "-");        // "Hello-World"
```

### Math Functions
```hixa
dhora number = -3.7;

dhora abs_val = abs_kora(number);            // 3.7
dhora rounded = round_kora(number);          // -4
dhora floored = floor_kora(number);          // -4
dhora ceiled = ceil_kora(number);            // -3
dhora sqrt_val = sqrt_kora(16);              // 4.0
dhora power = pow_kora(2, 8);                // 256
dhora sine = sin_kora(3.14159);              // ~0
dhora cosine = cos_kora(0);                  // 1.0
dhora tangent = tan_kora(0.785398);          // ~1
```

### Array Functions
```hixa
dhora numbers = [3, 1, 4, 1, 5];

dhora length = length_kora(numbers);         // 5
add_kora(numbers, 9);                        // Add to end
remove_kora(numbers, 1);                     // Remove first occurrence
sort_kora(numbers);                          // Sort in place
reverse_kora(numbers);                       // Reverse in place
dhora min_val = min_kora(numbers);           // Minimum value
dhora max_val = max_kora(numbers);           // Maximum value
dhora sum_val = sum_kora(numbers);           // Sum of all elements
dhora avg_val = average_kora(numbers);       // Average of elements
```

### Random Functions
```hixa
dhora random_num = random_kora(100);         // Random number 0-100
dhora random_int = random_kora(10, 20);      // Random integer 10-20
```

### Time Functions
```hixa
dhora current_time = time_kora();            // Current timestamp
sleep_kora(1.5);                             // Sleep for 1.5 seconds
```

### Utility Functions
```hixa
dhora range_nums = range_kora(10);           // [0, 1, 2, ..., 9]
dhora range_with_start = range_kora(5, 10);  // [5, 6, 7, 8, 9]
dhora range_with_step = range_kora(0, 10, 2); // [0, 2, 4, 6, 8]
```

## Examples

### Simple Calculator
```hixa
kam add_kora(x, y) {
    ghurai_diya (x + y);
}

kam subtract_kora(x, y) {
    ghurai_diya (x - y);
}

kam multiply_kora(x, y) {
    ghurai_diya (x * y);
}

kam divide_kora(x, y) {
    ghurai_diya (x / y);
}

kam main() {
    print_kora("Calculator Test Results:");
    print_kora("Addition: 10 + 5 = ");
    print_kora(add_kora(10, 5));
    
    print_kora("Subtraction: 10 - 5 = ");
    print_kora(subtract_kora(10, 5));
    
    print_kora("Multiplication: 10 * 5 = ");
    print_kora(multiply_kora(10, 5));
    
    print_kora("Division: 10 / 5 = ");
    print_kora(divide_kora(10, 5));
}
```

### Fibonacci Sequence
```hixa
kam fibonacci(n) {
    jodi (n <= 1) {
        ghurai_diya n;
    }
    ghurai_diya fibonacci(n - 1) + fibonacci(n - 2);
}

kam main() {
    print_kora("Fibonacci sequence:");
    dhora i = 0;
    jetialoike (i < 10); {
        dhora result = fibonacci(i);
        print_kora(result);
        i = i + 1;
    }
}
```

### String Processing
```hixa
kam process_text_kora(text) {
    dhora upper_text = upper_kora(text);
    dhora lower_text = lower_kora(text);
    dhora length = length_kora(text);
    
    print_kora("Original: ");
    print_kora(text);
    print_kora("Uppercase: ");
    print_kora(upper_text);
    print_kora("Lowercase: ");
    print_kora(lower_text);
    print_kora("Length: ");
    print_kora(length);
}

kam main() {
    process_text_kora("Hello Hixa World!");
}
```

### Array Operations
```hixa
kam array_demo_kora() {
    dhora numbers = [5, 2, 8, 1, 9, 3];
    
    print_kora("Original array: ");
    print_kora(numbers);
    
    sort_kora(numbers);
    print_kora("Sorted array: ");
    print_kora(numbers);
    
    reverse_kora(numbers);
    print_kora("Reversed array: ");
    print_kora(numbers);
    
    dhora sum_val = sum_kora(numbers);
    print_kora("Sum: ");
    print_kora(sum_val);
    
    dhora avg_val = average_kora(numbers);
    print_kora("Average: ");
    print_kora(avg_val);
}

kam main() {
    array_demo_kora();
}
```

## Best Practices

### Code Organization
1. **Use meaningful variable names**
2. **Group related functions together**
3. **Add comments for complex logic**
4. **Keep functions small and focused**

### Naming Conventions
```hixa
// Use descriptive names
dhora user_age = 25;                    // Good
dhora ua = 25;                          // Avoid

// Use consistent naming for functions
kam calculate_total_kora() { }          // Assamese style
fn calculate_total() { }                // English style
```

### Error Handling
```hixa
kam safe_divide_kora(a, b) {
    jodi (b == 0) {
        print_kora("Error: Division by zero!");
        ghurai_diya 0;
    }
    ghurai_diya (a / b);
}
```

### Performance Tips
1. **Avoid deep recursion for large inputs**
2. **Use appropriate data structures**
3. **Minimize function calls in loops**
4. **Cache frequently used values**

### Language Choice
- Use **Assamese keywords** for educational purposes or local context
- Use **English keywords** for international collaboration
- Be **consistent** within a single project

## Running Hixa Programs

### Command Line Interface
```bash
# Run a program
hixa run program.hx

# Check syntax without running
hixa check program.hx

# Format code (when implemented)
hixa format program.hx

# Start REPL
hixa repl

# Show version
hixa --version
```

### REPL (Interactive Mode)
```bash
hixa repl
```
Then you can type Hixa code interactively:
```hixa
>>> dhora x = 10
>>> print_kora(x)
10
>>> kam add(a, b) { ghurai_diya (a + b); }
>>> print_kora(add(5, 3))
8
```

## Troubleshooting

### Common Errors

#### "Expected ';' or newline after expression"
- Add semicolons after statements
- Check for missing semicolons in function calls

#### "Undefined variable"
- Ensure variables are declared before use
- Check variable scope

#### "Expected '(' after 'if'"
- Use parentheses around conditions: `jodi (condition)`

#### "Expected '{' before function body"
- Use curly braces for function bodies: `kam func() { }`

### Debugging Tips
1. Use `print_kora()` to debug variable values
2. Check syntax with `hixa check program.hx`
3. Start with simple examples and build complexity gradually
4. Use the REPL for testing small code snippets

## Conclusion

Hixa is a powerful educational programming language that bridges the gap between traditional programming languages and local language support. With its bilingual keyword system, rich standard library, and simple syntax, it's perfect for learning programming concepts while supporting cultural and linguistic diversity.

For more information, examples, and community support, visit the official Hixa documentation and community forums. 