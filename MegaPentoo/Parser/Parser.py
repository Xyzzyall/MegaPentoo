from enum import Enum
from MegaPentoo.Lexer.Tokens import TAGS

class STATES(Enum):
    ASSIGNING = 0

class Parser:
    def put_token(self, token):
        pass

    @staticmethod
    def __check_tag__(tag, expected):
        if expected == None:
            return False
        elif expected == TAGS.ID_OR_NUM_OR_OPERATION:
            return not (tag == TAGS.ID or tag == TAGS.AND or tag == TAGS.DIV or tag == TAGS.MULTI or \
                       tag == TAGS.PLUS or tag == TAGS.BOOL_EQUAL or tag == TAGS.NOT or tag == TAGS.OR or \
                       tag == TAGS.INT or tag == TAGS.TRUE or tag == TAGS.SKOBA_LEFT or tag == TAGS.SKOBA_RIGHT or \
                       tag == TAGS.MINUS or tag == TAGS.MORE or tag == TAGS.LESS or tag == TAGS.LESS_EQUAL or \
                       tag == TAGS.STRING or tag == TAGS.NEXT_CMD)
        else: return tag != expected

    def __if__(self, step):
        pass

    __program__ = []
    __str_buf__ = ""

    def analyze_tokens(self, tokens):
        expected_token = None
        state = None
        state_pos = 1

        for name, tag in tokens:
            if Parser.__check_tag__(tag, expected_token):
                raise NotExpected("Expected " + str(expected_token) + ", given " + str(tag))

            if state:
                if state == STATES.ASSIGNING:
                    if state_pos == 1:
                        expected_token = TAGS.ID_OR_NUM_OR_OPERATION
                        state_pos = 2
                    elif state_pos == 2:
                        if tag == TAGS.NEXT_CMD:
                            self.__program__.append(self.__str_buf__)
                            expected_token = None
                            state = None
                            state_pos = 0
                        else:
                            self.__str_buf__ += name
            else:
                if tag == TAGS.ID:
                    expected_token = TAGS.ASSIGN
                    self.__program__.append("write_to")
                    self.__program__.append(name)
                    state = STATES.ASSIGNING
                elif tag == TAGS.IF:
                    self.__program__.append("not_cond_goto")

    def get_program(self):
        return self.__program__


class NotExpected(Exception):
    pass


test = [
    ("a", TAGS.ID),
    ("=", TAGS.ASSIGN),
    ("1", TAGS.INT),
    ("+", TAGS.PLUS),
    ("2", TAGS.INT),
    ("\n", TAGS.NEXT_CMD)
]

t1 = Parser()
t1.analyze_tokens(test)
print(t1.get_program())