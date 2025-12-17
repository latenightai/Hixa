

<p align="center">
    <img src="https://github.com/latenightai/Hixa/blob/main/website/assets/logo-removebg-preview.png" alt="Hixa Logo">
</p>

<h3 align="center">A Modern Educational Programming Language with Bilingual Support</h3>

<p align="center">
	<img alt="stars" src="https://img.shields.io/github/stars/latenightai/Hixa?style=social" />
	<img alt="stars" src="https://img.shields.io/github/forks/latenightai/Hixa?style=social" />
	<img alt="stars" src="https://img.shields.io/github/watchers/latenightai/Hixa?style=social" />
</p>

## 🚀 Features

- **🌍 Bilingual Support**: Use English or Assamese keywords
- **📚 Educational Focus**: Designed for learning programming concepts
- **🔧 Rich Standard Library**: 50+ built-in functions with bilingual names
- **⚡ Simple Syntax**: C-like syntax with modern conveniences
- **🖥️ Cross-platform**: Runs on any system with Python 3.8+
- **🛠️ CLI Tools**: Command-line interface with REPL support

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Install
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

## 🚀 Quick Start

### Your First Hixa Program

Create a file named `hello.hx`:

```hixa
// Hello World in Hixa
kam main() {
    print_kora("Hello, World!");
    print_kora("Welcome to Hixa!");
}
```

Run it:
```bash
hixa run hello.hx
```

### Basic Syntax Examples

#### Variables and Functions
```hixa
// Variable declaration with Assamese keywords
dhora name = "Hixa";
dhora version = 1.0;

// Function definition
kam greet_kora(person) {
    print_kora("Hello, ");
    print_kora(person);
    print_kora("!");
}

kam main() {
    greet_kora(name);
}
```

#### Control Flow
```hixa
kam check_number(num) {
    jodi (num > 0) {
        print_kora("Positive number");
    } nohole jodi (num < 0) {
        print_kora("Negative number");
    } nohole {
        print_kora("Zero");
    }
}
```

#### Loops
```hixa
kam count() {
    dhora i = 1;
    jetialoike (i <= 5); {
        print_kora(i);
        i = i + 1;
    }
}
```

## 📚 Language Features

### Bilingual Keywords

| English | Assamese | Description |
|---------|----------|-------------|
| `fn` | `kam` | Function declaration |
| `let` | `dhora` | Variable declaration |
| `if` | `jodi` | Conditional statement |
| `else` | `nohole` | Alternative condition |
| `while` | `jetialoike` | Loop statement |
| `return` | `ghurai_diya` | Return value |
| `true` | `hosa` | Boolean true |
| `false` | `misa` | Boolean false |
| `print` | `print_kora` | Print function |

### Data Types
- **Numbers**: `42`, `3.14`, `-10`
- **Strings**: `"Hello"`, `'World'`
- **Booleans**: `hosa` (true), `misa` (false)
- **Arrays**: `[1, 2, 3, 4, 5]`
- **Null**: `nai`

### Standard Library Functions

#### Input/Output
```hixa
print_kora("Hello");           // Print to console
dhora input = input_lou("Enter name: ");  // Get user input
```

#### String Operations
```hixa
dhora text = "Hello World";
dhora upper = upper_kora(text);    // "HELLO WORLD"
dhora lower = lower_kora(text);    // "hello world"
dhora length = length_kora(text);  // 11
```

#### Math Functions
```hixa
dhora sqrt_val = sqrt_kora(16);    // 4.0
dhora power = pow_kora(2, 8);      // 256
dhora abs_val = abs_kora(-42);     // 42
```

#### Array Operations
```hixa
dhora numbers = [3, 1, 4, 1, 5];
sort_kora(numbers);                // Sort in place
dhora sum_val = sum_kora(numbers); // Sum of elements
dhora avg_val = average_kora(numbers); // Average
```

## 🛠️ Command Line Interface

```bash
# Run a program
hixa run program.hx

# Check syntax without running
hixa check program.hx

# Start interactive REPL
hixa repl

# Show version
hixa --version
```

## 📖 Examples

### Calculator
```hixa
kam add_kora(x, y) {
    ghurai_diya (x + y);
}

kam subtract_kora(x, y) {
    ghurai_diya (x - y);
}

kam main() {
    print_kora("Calculator Test:");
    print_kora("10 + 5 = ");
    print_kora(add_kora(10, 5));
    print_kora("10 - 5 = ");
    print_kora(subtract_kora(10, 5));
}
```

## 📚 Documentation

For comprehensive documentation, see:
- [📖 Complete Language Guide](docs/HIXA_LANGUAGE_GUIDE.md)
- [📝 Examples Directory](examples/)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python run_tests.py

# Format code
black src/
isort src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 What's New?

- **v1.0.0**: Initial release with bilingual keyword support
- Rich standard library with 50+ functions
- Command-line interface with REPL
- Comprehensive documentation
- Educational examples and tutorials


## 📞 Support

- 📧 Email: latenightai.yt@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/hixa-lang/hixa/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/hixa-lang/hixa/discussions)

---

<p align="center">Made with ❤️ for the programming education community</p>
