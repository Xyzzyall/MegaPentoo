from enum import Enum
from MegaPentoo.Lexer.Tokens import TAGS


class STATES(Enum):
    ASSIGNING = 0
    IF = 1
    WHILE = 2
    PRINT = 3
    INPUT = 4
    LIST = 5
    SET = 6


class Parser:
    def put_token(self, token):
        pass

    @staticmethod
    def __check_tag__(tag, expected):
        not_command = tag == TAGS.ID or tag == TAGS.AND or tag == TAGS.DIV or tag == TAGS.MULTI or \
                       tag == TAGS.PLUS or tag == TAGS.BOOL_EQUAL or tag == TAGS.NOT or tag == TAGS.OR or \
                       tag == TAGS.INT or tag == TAGS.TRUE or tag == TAGS.SKOBA_LEFT or tag == TAGS.SKOBA_RIGHT or \
                       tag == TAGS.MINUS or tag == TAGS.MORE or tag == TAGS.LESS or tag == TAGS.LESS_EQUAL or \
                       tag == TAGS.STRING or tag == TAGS.CLASS_OBJECT

        command = not (tag == TAGS.AND or tag == TAGS.DIV or tag == TAGS.MULTI or \
                       tag == TAGS.PLUS or tag == TAGS.BOOL_EQUAL or tag == TAGS.NOT or tag == TAGS.OR or \
                       tag == TAGS.INT or tag == TAGS.TRUE or tag == TAGS.SKOBA_LEFT or tag == TAGS.SKOBA_RIGHT or \
                       tag == TAGS.MINUS or tag == TAGS.MORE or tag == TAGS.LESS or tag == TAGS.LESS_EQUAL or \
                       tag == TAGS.STRING)

        if not expected:
            return False
        elif expected == TAGS.ID_OR_NUM_OR_OPERATION:
            return not not_command and not tag == TAGS.NEXT_CMD
        elif expected == TAGS.IF_CHECK:
            return (not not_command) and (not TAGS.THEN)
        elif expected == TAGS.WHILE_CHECK:
            return (not not_command) and (not TAGS.DO)
        elif expected == TAGS.COMMAND:
            return not command
        else:
            return tag != expected

    def __if__(self, step):
        pass

    __program__ = []
    __str_buf__ = ""

    def analyze_tokens(self, tokens):
        expected_token = None
        state = None
        state_pos = 1

        i = 0

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
                            self.__append_command__(self.__str_buf__)
                            self.__str_buf__ = ""
                            expected_token = None
                            state = None
                            state_pos = 1
                        else:
                            self.__str_buf__ += name
                elif state == STATES.IF:
                    if state_pos == 1:
                        self.__str_buf__ += name
                        expected_token = TAGS.IF_CHECK
                        state_pos = 2
                    elif state_pos == 2:
                        if tag == TAGS.THEN:
                            self.__append_command__(self.__str_buf__)
                            self.__append_command__("not_cond_goto")
                            self.__push_backturn__(TAGS.IF)
                            self.__append_command__(None)
                            state = None
                            self.__str_buf__ = ""
                            expected_token = TAGS.COMMAND
                            state_pos = 1
                        else:
                            self.__str_buf__ += name
                elif state == STATES.WHILE:
                    if state_pos == 1:
                        self.__str_buf__ += name
                        expected_token = TAGS.WHILE_CHECK
                        state_pos = 2
                    elif state_pos == 2:
                        if tag == TAGS.DO:
                            self.__append_command__(self.__str_buf__)
                            self.__append_command__("not_cond_goto")
                            self.__push_backturn__(TAGS.WHILE)
                            self.__append_command__(None)
                            state = None
                            self.__str_buf__ = ""
                            expected_token = TAGS.COMMAND
                            state_pos = 1
                        else:
                            self.__str_buf__ += name
                elif state == STATES.PRINT:
                    if tag == TAGS.NEXT_CMD:
                        self.__append_command__(self.__str_buf__)
                        self.__str_buf__ = ""
                        expected_token = None
                        state = None
                    else:
                        self.__str_buf__ += name
                elif state == STATES.INPUT:
                    if tag == TAGS.NEXT_CMD:
                        self.__append_command__(self.__str_buf__)
                        self.__str_buf__ = ""
                        expected_token = None
                        state = None
                    else:
                        self.__str_buf__ += name
                elif state == STATES.LIST:
                    self.__append_command__(name + "=Elem(0,None,None)")
                    state = None
                    expected_token = None
                elif state == STATES.SET:
                    self.__append_command__(name + "=HashSet()")
                    state = None
                    expected_token = None
            else:
                if tag == TAGS.ID:
                    expected_token = TAGS.ASSIGN
                    self.__append_command__("write_to")
                    self.__append_command__(name)
                    state = STATES.ASSIGNING
                elif tag == TAGS.IF:
                    self.__append_command__("write_cond")
                    state = STATES.IF
                    expected_token = TAGS.ID_OR_NUM_OR_OPERATION
                elif tag == TAGS.END:
                    b_tag, b_pos1, b_pos2 = self.__pop_backturn__()
                    if b_tag == TAGS.IF:
                        self.__program__[b_pos2] = str(self.__cur_cmd__)
                    elif b_tag == TAGS.WHILE:
                        self.__append_command__("goto")
                        self.__append_command__(str(b_pos1-2))
                        self.__program__[b_pos2] = str(self.__cur_cmd__)
                elif tag == TAGS.WHILE:
                    self.__append_command__("write_cond")
                    state = STATES.WHILE
                    expected_token = TAGS.ID_OR_NUM_OR_OPERATION
                elif tag == TAGS.PENTOO:
                    self.__append_command__("print")
                    expected_token = TAGS.ID_OR_NUM_OR_OPERATION
                    state = STATES.PRINT
                elif tag == TAGS.LOOKIN:
                    self.__append_command__("input")
                    expected_token = TAGS.ID_OR_NUM_OR_OPERATION
                    state = STATES.INPUT
                elif tag == TAGS.CLASS_OBJECT:
                    self.__append_command__("direct")
                    self.__append_command__(name)
                elif tag == TAGS.LINKED_LIST:
                    expected_token = TAGS.ID
                    state = STATES.LIST
                    self.__append_command__("direct")
                elif tag == TAGS.HASH_SET:
                    expected_token = TAGS.ID
                    state = STATES.SET
                    self.__append_command__("direct")



    __backturns_stack__ = list()

    __cur_cmd__ = 0

    def __append_command__(self, cmd):
        self.__program__.append(cmd)
        self.__cur_cmd__ += 1

    def __push_backturn__(self, tag):
        self.__backturns_stack__.append((tag, len(self.__program__)-1, len(self.__program__)))

    def __pop_backturn__(self):
        return self.__backturns_stack__.pop()

    def get_program(self):
        return self.__program__


class NotExpected(Exception):
    pass



