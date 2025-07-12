"""
Command-line interface for the Hixa programming language.

This module provides the main entry point for running Hixa programs
from the command line.
"""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .stdlib import StandardLibrary


console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="Hixa")
def main():
    """
    Hixa Programming Language
    
    A modern, production-ready programming language implemented in Python.
    """
    pass


@main.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--show-tokens', is_flag=True, help='Show lexed tokens')
@click.option('--show-ast', is_flag=True, help='Show parsed AST')
def run(file: Path, verbose: bool, show_tokens: bool, show_ast: bool):
    """Run a Hixa program file."""
    try:
        # Read source code
        with open(file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        if verbose:
            console.print(f"[bold blue]Running:[/bold blue] {file}")
            console.print(f"[bold blue]Source length:[/bold blue] {len(source)} characters")
        
        # Lexical analysis
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            disable=not verbose
        ) as progress:
            task = progress.add_task("Lexical analysis...", total=None)
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            progress.update(task, description="Lexical analysis complete")
        
        if show_tokens:
            console.print("\n[bold]Tokens:[/bold]")
            for token in tokens:
                console.print(f"  {token}")
        
        if lexer.errors:
            console.print(f"\n[bold red]Lexical errors:[/bold red]")
            for error in lexer.errors:
                console.print(f"  [red]{error}[/red]")
            sys.exit(1)
        
        # Parsing
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            disable=not verbose
        ) as progress:
            task = progress.add_task("Parsing...", total=None)
            parser = Parser(tokens)
            ast = parser.parse()
            progress.update(task, description="Parsing complete")
        
        if show_ast:
            console.print("\n[bold]AST:[/bold]")
            console.print(ast)
        
        if parser.errors:
            console.print(f"\n[bold red]Parsing errors:[/bold red]")
            for error in parser.errors:
                console.print(f"  [red]{error}[/red]")
            sys.exit(1)
        
        # Interpretation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            disable=not verbose
        ) as progress:
            task = progress.add_task("Executing...", total=None)
            interpreter = Interpreter()
            interpreter.interpret(ast.statements)
            progress.update(task, description="Execution complete")
        
        if verbose:
            console.print(f"\n[bold green]Program completed successfully![/bold green]")
    
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File '{file}' not found")
        sys.exit(1)
    except PermissionError:
        console.print(f"[bold red]Error:[/bold red] Permission denied reading '{file}'")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@main.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
def check(file: Path):
    """Check syntax of a Hixa program file without executing it."""
    try:
        # Read source code
        with open(file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        console.print(f"[bold blue]Checking syntax:[/bold blue] {file}")
        
        # Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if lexer.errors:
            console.print(f"\n[bold red]Lexical errors:[/bold red]")
            for error in lexer.errors:
                console.print(f"  [red]{error}[/red]")
            sys.exit(1)
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        if parser.errors:
            console.print(f"\n[bold red]Parsing errors:[/bold red]")
            for error in parser.errors:
                console.print(f"  [red]{error}[/red]")
            sys.exit(1)
        
        console.print(f"[bold green]✓ Syntax check passed![/bold green]")
        console.print(f"  - {len(tokens)} tokens")
        console.print(f"  - {len(ast.statements)} statements")
    
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File '{file}' not found")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@main.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
def format(file: Path):
    """Format a Hixa program file."""
    try:
        # Read source code
        with open(file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        console.print(f"[bold blue]Formatting:[/bold blue] {file}")
        
        # For now, just show the source with syntax highlighting
        # TODO: Implement actual formatting
        syntax = Syntax(source, "hixa", theme="monokai")
        console.print(Panel(syntax, title="Formatted Code"))
        
        console.print(f"[bold green]✓ Formatting complete![/bold green]")
        console.print(f"[yellow]Note:[/yellow] Actual formatting not yet implemented")
    
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File '{file}' not found")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@main.command()
def repl():
    """Start the Hixa REPL (Read-Eval-Print Loop)."""
    console.print("[bold blue]Hixa REPL[/bold blue]")
    console.print("Type 'exit' or 'quit' to exit, 'help' for help")
    console.print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            # Get input
            line = input("hixa> ").strip()
            
            if line.lower() in ['exit', 'quit']:
                console.print("[bold green]Goodbye![/bold green]")
                break
            
            if line.lower() == 'help':
                console.print("[bold]Available commands:[/bold]")
                console.print("  exit, quit - Exit the REPL")
                console.print("  help - Show this help")
                console.print("  clear - Clear the screen")
                console.print()
                continue
            
            if line.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                continue
            
            if not line:
                continue
            
            # Add semicolon if missing
            if not line.endswith(';'):
                line += ';'
            
            # Lexical analysis
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            
            if lexer.errors:
                for error in lexer.errors:
                    console.print(f"[red]Lexical error: {error}[/red]")
                continue
            
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            
            if parser.errors:
                for error in parser.errors:
                    console.print(f"[red]Parsing error: {error}[/red]")
                continue
            
            # Interpretation
            try:
                result = interpreter.interpret(ast.statements)
                if result is not None:
                    console.print(f"[green]Result: {result}[/green]")
            except Exception as e:
                console.print(f"[red]Runtime error: {e}[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[bold green]Goodbye![/bold green]")
            break
        except EOFError:
            console.print("\n[bold green]Goodbye![/bold green]")
            break


@main.command()
def init():
    """Initialize a new Hixa project."""
    project_name = click.prompt("Project name", default="my-hixa-project")
    
    # Create project directory
    project_dir = Path(project_name)
    if project_dir.exists():
        console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists")
        sys.exit(1)
    
    project_dir.mkdir()
    
    # Create main source file
    main_file = project_dir / "main.hx"
    with open(main_file, 'w') as f:
        f.write("""fn main() {
    print("Hello, Hixa!")
    
    let name = "World"
    print("Hello, {name}!")
    
    let numbers = [1, 2, 3, 4, 5]
    let sum = 0
    
    for i in range(len(numbers)) {
        sum = sum + numbers[i];
    }
    
    print("Sum: {sum}");
}

main();
""")
    
    # Create README
    readme_file = project_dir / "README.md"
    with open(readme_file, 'w') as f:
        f.write(f"""# {project_name}

A Hixa programming language project.

## Running

```bash
hixa run main.hx
```

## Syntax Check

```bash
hixa check main.hx
```
""")
    
    console.print(f"[bold green]✓ Project '{project_name}' created successfully![/bold green]")
    console.print(f"  - Created directory: {project_dir}")
    console.print(f"  - Created main file: {main_file}")
    console.print(f"  - Created README: {readme_file}")
    console.print()
    console.print("To run your project:")
    console.print(f"  cd {project_name}")
    console.print("  hixa run main.hx")


@main.command()
def version():
    """Show version information."""
    console.print("[bold blue]Hixa Programming Language[/bold blue]")
    console.print("Version: 0.1.0")
    console.print("Python: " + sys.version)
    console.print("Platform: " + sys.platform)


if __name__ == '__main__':
    main() 