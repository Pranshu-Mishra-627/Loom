from enum import Enum, auto
from dataclasses import dataclass as DC

class TokenType(Enum):
    NAME = auto()
    NUMBER = auto()
    STRING = auto()
    EMOTION_TAG = auto()

    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    DEF = auto()
    RETURN = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    NONE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    MOD = auto()

    ASSIGN = auto()

    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()

    COMMA = auto()
    SEMICOLON = auto()

    EOF = auto()

@DC 
class TokenInfo:
    type:TokenType
    value: str
    emotion:str = None

