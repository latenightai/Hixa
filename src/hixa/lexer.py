"""
Lexical analyzer for the Hixa programming language.

This module handles tokenization of source code, converting text into
a stream of tokens that can be parsed by the parser.
"""

from enum import Enum, auto
from typing import List, Optional
import re


class TokenType(Enum):
    """Token types for the Hixa language."""
    
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()
    
    # Keywords - Core Control Flow
    KAM = auto()  # function
    GHAURAI_DIYA = auto()  # return
    JODI = auto()  # if
    NOHOLE = auto()  # else
    NAHOLE = auto()  # elif
    JETIALOIKE = auto()  # while
    KARONE = auto()  # for
    HEKH = auto()  # end
    
    # Boolean Keywords
    HOSA = auto()  # true
    MISA = auto()  # false
    NAI = auto()  # null
    ARU = auto()  # and
    BA = auto()  # or
    NOT_KORA = auto()  # not
    
    # Variable and Type Keywords
    DHORA = auto()  # let/var
    LIST = auto()  # list
    DICTIONARY = auto()  # dict
    
    # Loop Control
    BREAK_KORA = auto()  # break
    CONTINUE_KORA = auto()  # continue
    
    # Module and Program Structure
    IMPORT = auto()  # import
    MAIN = auto()  # main
    PASS_KORA = auto()  # pass
    
    # I/O Operations
    INPUT_LOU = auto()  # input
    PRINT_KORA = auto()  # print
    POHA = auto()  # read
    LIKHA = auto()  # write
    OPEN_KORA = auto()  # open
    CLOSE_KORA = auto()  # close
    
    # Utility Functions
    RANDOM_KORA = auto()  # random
    TIME_KORA = auto()  # time
    SLEEP_KORA = auto()  # sleep
    CLEAR_KORA = auto()  # clear
    
    # List/String Operations
    LENGTH_KORA = auto()  # len
    ADD_KORA = auto()  # append
    REMOVE_KORA = auto()  # remove
    SORT_KORA = auto()  # sort
    REVERSE_KORA = auto()  # reverse
    BISORA = auto()  # find
    REPLACE_KORA = auto()  # replace
    SPLIT_KORA = auto()  # split
    JOIN_KORA = auto()  # join
    UPPER_KORA = auto()  # upper
    LOWER_KORA = auto()  # lower
    
    # Math Functions
    ROUND_KORA = auto()  # round
    FLOOR_KORA = auto()  # floor
    CEIL_KORA = auto()  # ceil
    ABS_KORA = auto()  # abs
    SQRT_KORA = auto()  # sqrt
    POW_KORA = auto()  # pow
    SIN_KORA = auto()  # sin
    COS_KORA = auto()  # cos
    TAN_KORA = auto()  # tan
    LOG_KORA = auto()  # log
    EXP_KORA = auto()  # exp
    MIN_KORA = auto()  # min
    MAX_KORA = auto()  # max
    SUM_KORA = auto()  # sum
    AVERAGE_KORA = auto()  # average
    COUNT_KORA = auto()  # count
    
    # Object/Data Operations
    COPY_KORA = auto()  # copy
    DELETE_KORA = auto()  # delete
    CHECK_KORA = auto()  # check
    CONVERT_KORA = auto()  # convert
    FORMAT_KORA = auto()  # format
    VALIDATE_KORA = auto()  # validate
    
    # Error Handling
    ERROR_KORA = auto()  # error
    TRY_KORA = auto()  # try
    CATCH_KORA = auto()  # catch
    FINALLY_KORA = auto()  # finally
    
    # Legacy English Keywords (for backward compatibility)
    LET = auto()
    FN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    CLASS = auto()
    SELF = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    ARROW = auto()
    PIPE = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


class Token:
    """Represents a token in the source code."""
    
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self) -> str:
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.line == other.line and 
                self.column == other.column)


class Lexer:
    """Lexical analyzer for Hixa source code."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[str] = []
        
        # Regular expressions for different token types
        self.patterns = [
            (TokenType.COMMENT, r'//.*'),
            (TokenType.STRING, r'"[^"]*"'),
            (TokenType.FLOAT, r'\d+\.\d+'),
            (TokenType.INT, r'\d+'),
            (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
            (TokenType.ARROW, r'->'),
            (TokenType.LESS_EQUAL, r'<='),
            (TokenType.GREATER_EQUAL, r'>='),
            (TokenType.NOT_EQUAL, r'!='),
            (TokenType.EQUAL, r'=='),
            (TokenType.ASSIGN, r'='),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.MODULO, r'%'),
            (TokenType.LESS, r'<'),
            (TokenType.GREATER, r'>'),
            (TokenType.AND, r'&&'),
            (TokenType.OR, r'\|\|'),
            (TokenType.NOT, r'!'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.LBRACE, r'\{'),
            (TokenType.RBRACE, r'\}'),
            (TokenType.LBRACKET, r'\['),
            (TokenType.RBRACKET, r'\]'),
            (TokenType.SEMICOLON, r';'),
            (TokenType.COMMA, r','),
            (TokenType.DOT, r'\.'),
            (TokenType.COLON, r':'),
            (TokenType.PIPE, r'\|'),
        ]
        
        # Keywords mapping - Assamese-English reserved words only
        self.keywords = {
            # Core Control Flow
            'kam': TokenType.KAM,
            'ghurai_diya': TokenType.GHAURAI_DIYA,
            'jodi': TokenType.JODI,
            'nohole': TokenType.NOHOLE,
            'nahole': TokenType.NAHOLE,
            'jetialoike': TokenType.JETIALOIKE,
            'karone': TokenType.KARONE,
            'hekh': TokenType.HEKH,
            # Boolean/Null/Logic
            'hosa': TokenType.HOSA,
            'misa': TokenType.MISA,
            'nai': TokenType.NAI,
            'aru': TokenType.ARU,
            'ba': TokenType.BA,
            'not_kora': TokenType.NOT_KORA,
            # Variable declaration
            'dhora': TokenType.DHORA,
            # Loop Control
            'break_kora': TokenType.BREAK_KORA,
            'continue_kora': TokenType.CONTINUE_KORA,
            # Module and Program Structure
            'import': TokenType.IMPORT,
            'pass_kora': TokenType.PASS_KORA,
            # Error Handling
            'error_kora': TokenType.ERROR_KORA,
            'try_kora': TokenType.TRY_KORA,
            'catch_kora': TokenType.CATCH_KORA,
            'finally_kora': TokenType.FINALLY_KORA,
            # Legacy English Keywords (for backward compatibility)
            'let': TokenType.LET,
            'fn': TokenType.FN,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'return': TokenType.RETURN,
            'class': TokenType.CLASS,
            'self': TokenType.SELF,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL,
            'print': TokenType.PRINT_KORA,
        }
    
    def tokenize(self) -> List[Token]:
        """Convert source code into a list of tokens."""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            token = self._get_next_token()
            if token:
                if token.type != TokenType.COMMENT:  # Skip comments
                    self.tokens.append(token)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while (self.position < len(self.source) and 
               self.source[self.position].isspace()):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def _get_next_token(self) -> Optional[Token]:
        """Get the next token from the source."""
        current_char = self.source[self.position]
        
        # Handle comments
        if current_char == '/' and (self.position + 1 < len(self.source) and 
                                   self.source[self.position + 1] == '/'):
            return self._handle_comment()
        
        # Try to match patterns
        for token_type, pattern in self.patterns:
            match = re.match(pattern, self.source[self.position:])
            if match:
                value = match.group(0)
                token = self._create_token(token_type, value)
                self.position += len(value)
                self.column += len(value)
                return token
        
        # If no pattern matches, it's an error
        raise SyntaxError(f"Unexpected character '{current_char}' at line {self.line}, column {self.column}")
    
    def _handle_comment(self) -> Token:
        """Handle single-line comments."""
        start_pos = self.position
        while (self.position < len(self.source) and 
               self.source[self.position] != '\n'):
            self.position += 1
        
        comment = self.source[start_pos:self.position]
        token = Token(TokenType.COMMENT, comment, self.line, self.column)
        self.column += len(comment)
        return token
    
    def _create_token(self, type_: TokenType, value: str) -> Token:
        """Create a token with proper type conversion."""
        # Handle keywords
        if type_ == TokenType.IDENTIFIER and value in self.keywords:
            type_ = self.keywords[value]
        
        # Handle string literals (remove quotes)
        if type_ == TokenType.STRING:
            value = value[1:-1]  # Remove surrounding quotes
        
        return Token(type_, value, self.line, self.column) 