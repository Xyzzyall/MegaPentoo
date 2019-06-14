from enum import Enum


class TAGS(Enum):
    NEXT_CMD = 0
    COMMA = 1
    PLUS = 2
    MINUS = 3
    MULTI = 4
    DIV = 5
    LESS_EQUAL = 6
    LESS = 7
    MORE_EQUAL = 8
    MORE = 9
    BOOL_EQUAL = 10
    NON_EQUAL = 11
    AND = 12
    OR = 13
    NOT = 14
    TRUE = 15
    FALSE = 16
    IF = 17
    ASSIGN = 18
    SKOBA_LEFT = 19
    SKOBA_RIGHT = 20
    THEN = 21
    WHILE = 22
    BEGIN = 23
    END = 24
    DO = 25
    RETURN = 26
    PENTOO = 27
    LOOKIN = 28
    PROGA = 29
    INT = 30
    ID = 31
    STRING = 32

token_exprs = [
    (r'[ \t]+',    None),
    (r'//[^\n]*',  None),
    (r'=',                     TAGS.ASSIGN),
    (r'\(',                    TAGS.SKOBA_LEFT),
    (r'\)',                    TAGS.SKOBA_RIGHT),
    (r'\n',                    TAGS.NEXT_CMD),
    (r',',                     TAGS.COMMA),
    (r'\+',                    TAGS.PLUS),
    (r'-',                     TAGS.MINUS),
    (r'\*',                    TAGS.MULTI),
    (r'/',                     TAGS.DIV),
    (r'<=',                    TAGS.LESS_EQUAL),
    (r'<',                     TAGS.LESS),
    (r'>=',                    TAGS.MORE_EQUAL),
    (r'>',                     TAGS.MORE),
    (r'==',                    TAGS.BOOL_EQUAL),
    (r'!=',                    TAGS.NON_EQUAL),
    (r'and',                   TAGS.AND),
    (r'or',                    TAGS.OR),
    (r'not',                   TAGS.NOT),
    (r'true',                  TAGS.TRUE),
    (r'false',                 TAGS.FALSE),
    (r'if',                    TAGS.IF),
    (r'then',                  TAGS.THEN),
#    (r'else',                  RESERVED),
    (r'while',                 TAGS.WHILE),
    (r'begin',                 TAGS.BEGIN),
    (r'end',                   TAGS.END),
    (r'do',                    TAGS.DO),
    (r'return',                TAGS.RETURN),
    (r'pentoo',                TAGS.PENTOO),   # print analog
    (r'lookin',                TAGS.LOOKIN),   # write analog
    (r'proga',                 TAGS.PROGA),   # function analog
    (r'[0-9]+',                TAGS.INT),
    (r'[A-Za-z][A-Za-z0-9_]*', TAGS.ID),
    (r'".+"',                  TAGS.STRING),
]