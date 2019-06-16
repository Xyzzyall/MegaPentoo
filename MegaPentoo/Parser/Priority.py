from MegaPentoo.Lexer.Tokens import *


class PRIORITY:
    @staticmethod
    def get_priority(tag):
        if tag == TAGS.PLUS:
            return PRIORITY.PLUS
        elif tag == TAGS.MINUS:
            return PRIORITY.MINUS
        elif tag == TAGS.MULTI:
            return PRIORITY.MULT
        elif tag == TAGS.DIV:
            return PRIORITY.DIV
        elif tag == TAGS.LESS:
            return PRIORITY.LESS
        elif tag == TAGS.MORE:
            return PRIORITY.MORE
        elif tag == TAGS.BOOL_EQUAL:
            return PRIORITY.BOOL_EQUAL
        elif tag == TAGS.NON_EQUAL:
            return PRIORITY.NON_EQUAL
        elif tag == TAGS.AND:
            return PRIORITY.AND
        elif tag == TAGS.OR:
            return PRIORITY.OR
        elif tag == TAGS.NOT:
            return PRIORITY.NOT
        else:
            return 0

    PLUS = 200
    MINUS = 200
    MULT = 201
    DIV = 201
    LESS_EQUAL = 102
    LESS = 102
    MORE_EQUAL = 102
    MORE = 102
    BOOL_EQUAL = 102
    NON_EQUAL = 102
    AND = 100
    OR = 100
    NOT = 101
    SKOBA_LEFT = 0
    SKOBA_RIGHT = 0
