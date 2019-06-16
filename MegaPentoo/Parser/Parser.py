from enum import Enum
from MegaPentoo.Lexer.Tokens import TAGS
from MegaPentoo.Parser.Priority import PRIORITY
from MegaPentoo.Interpretator.HashSet import HashSet
from MegaPentoo.VM.VM import COMMANDS


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
    __tag_buf__ = []
    __var_set__ = dict()
    __var_counter__ = 0

    def get_id_address(self, id):
        if id in self.__var_set__:
            return self.__var_set__[id] + 1
        else:
            self.__var_set__[id] = self.__var_counter__
            self.__var_counter__ += 1
            return self.__var_set__[id] + 1

    def to_polska(self, tokens):
        res = []
        stack = []
        for name, tag in tokens:
            if tag == TAGS.ID:
                res.append(COMMANDS.PUSH_VAR)
                res.append(self.get_id_address(name))
            elif tag == TAGS.INT:
                res.append(COMMANDS.PUSH)
                res.append(name)
            elif tag == TAGS.TRUE or tag == TAGS.FALSE:
                res.append(COMMANDS.PUSH)
                res.append(name)
            elif tag == TAGS.SKOBA_LEFT:
                stack.append(tag)
            elif tag == TAGS.SKOBA_RIGHT:
                v = stack.pop()
                while v != TAGS.SKOBA_LEFT or len(res) != 0:
                    res.append(v)
            else:
                priority = PRIORITY.get_priority(tag)
                while len(stack) > 0 and PRIORITY.get_priority(stack[len(stack) - 1]) >= priority:
                    res.append(stack.pop())
                stack.append(tag)

        while len(stack) > 0:
            res.append(stack.pop())

        res.append(COMMANDS.DONE)
        return res

    def translate_to_commands(self, polska):
        res = []
        for e in polska:
            if type(e) is tuple:
                e = e[1]

            if type(e) is TAGS:
                if e == TAGS.PLUS:
                    res.append(COMMANDS.PLUS)
                elif e == TAGS.MINUS:
                    res.append(COMMANDS.MINUS)
                elif e == TAGS.MULTI:
                    res.append(COMMANDS.MULT)
                elif e == TAGS.DIV:
                    res.append(COMMANDS.DIV)
                elif e == TAGS.LESS:
                    res.append(COMMANDS.MINUS)
                    res.append(COMMANDS.POP)
                    res.append(COMMANDS.PUSH_FLAG_NEG)
                    #res.append(COMMANDS.COND_LESS)
                elif e == TAGS.MORE:
                    res.append(COMMANDS.MINUS)
                    res.append(COMMANDS.POP)
                    res.append(COMMANDS.PUSH_FLAG_POS)
                    #res.append(COMMANDS.COND_MORE)
                elif e == TAGS.BOOL_EQUAL:
                    res.append(COMMANDS.MINUS)
                    res.append(COMMANDS.POP)
                    res.append(COMMANDS.PUSH_FLAG_ZERO)
                    #res.append(COMMANDS.BOOL_EQUAL)
                elif e == TAGS.NON_EQUAL:
                    res.append(COMMANDS.MINUS)
                    res.append(COMMANDS.POP)
                    res.append(COMMANDS.PUSH_FLAG_NOT_ZERO)
                    #res.append(COMMANDS.NON_EQUAL)
                elif e == TAGS.AND:
                    res.append(COMMANDS.COND_AND)
                elif e == TAGS.OR:
                    res.append(COMMANDS.COND_OR)
                elif e == TAGS.NOT:
                    res.append(COMMANDS.COND_NOT)
            else:
                if e == "write_to":
                    res.append(COMMANDS.WRITE_TO)
                elif e == "write_cond":
                    res.append(COMMANDS.WRITE_TO_CONDITION)
                elif e == "goto":
                    res.append(COMMANDS.GOTO)
                elif e == "not_cond_goto":
                    res.append(COMMANDS.GOTO_NOT_CONDITION)
                elif e == "cond_goto":
                    res.append(COMMANDS.GOTO_CONDITION)
                elif e == "input":
                    res.append(COMMANDS.INPUT)
                elif e == "print":
                    res.append(COMMANDS.PRINT)
                else:
                    res.append(e)

        return res

    def analyze_tokens(self, tokens, mode=1):
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
                            if mode:
                                self.__append_command__(self.translate_to_commands(self.to_polska(self.__tag_buf__)))
                                self.__tag_buf__ = []
                            else:
                                self.__append_command__(self.__str_buf__)
                                self.__str_buf__ = ""
                            expected_token = None
                            state = None
                            state_pos = 1
                        else:
                            if mode:
                                self.__tag_buf__.append((name, tag))
                            else:
                                if tag == TAGS.AND or tag == TAGS.OR:
                                    self.__str_buf__ += ' ' + name + ' '
                                else:
                                    self.__str_buf__ += name
                elif state == STATES.IF:
                    if state_pos == 1:
                        if mode:
                            self.__tag_buf__ = [(name, tag)]
                        else:
                            self.__str_buf__ += name
                        expected_token = TAGS.IF_CHECK
                        state_pos = 2
                    elif state_pos == 2:
                        offset = len(self.__program__) + 1
                        if tag == TAGS.THEN:
                            if mode:
                                self.__append_command__(self.translate_to_commands(self.to_polska(self.__tag_buf__)))
                                self.__tag_buf__ = []
                            else:
                                self.__append_command__(self.__str_buf__)
                                self.__str_buf__ = ""
                            offset -= len(self.__program__)
                            self.__append_command__("not_cond_goto")
                            self.__push_backturn__(TAGS.IF, -offset)
                            self.__append_command__(None)
                            state = None
                            expected_token = TAGS.COMMAND
                            state_pos = 1
                        else:
                            if mode:
                                self.__tag_buf__.append((name, tag))
                            else:
                                if tag == TAGS.AND or tag == TAGS.OR:
                                    self.__str_buf__ += ' ' + name + ' '
                                else:
                                    self.__str_buf__ += name
                elif state == STATES.WHILE:
                    if state_pos == 1:
                        if mode:
                            self.__tag_buf__ = [(name, tag)]
                        else:
                            self.__str_buf__ += name
                        expected_token = TAGS.WHILE_CHECK
                        state_pos = 2
                    elif state_pos == 2:
                        if tag == TAGS.DO:
                            offset = len(self.__program__) + 1
                            if mode:
                                self.__append_command__(self.translate_to_commands(self.to_polska(self.__tag_buf__)))
                                self.__tag_buf__ = []
                            else:
                                self.__append_command__(self.__str_buf__)
                                self.__str_buf__ = ""
                            offset -= len(self.__program__)
                            self.__append_command__("not_cond_goto")
                            self.__push_backturn__(TAGS.WHILE, -offset)
                            self.__append_command__(None)
                            state = None
                            self.__str_buf__ = ""
                            expected_token = TAGS.COMMAND
                            state_pos = 1
                        else:
                            if mode:
                                self.__tag_buf__.append((name, tag))
                            else:
                                if tag == TAGS.AND or tag == TAGS.OR:
                                    self.__str_buf__ += ' ' + name + ' '
                                else:
                                    self.__str_buf__ += name
                elif state == STATES.PRINT:
                    if tag == TAGS.NEXT_CMD:
                        if mode:
                            self.__append_command__(self.translate_to_commands(self.to_polska(self.__tag_buf__)))
                            self.__tag_buf__ = []
                        else:
                            self.__append_command__(self.__str_buf__)
                            self.__str_buf__ = ""
                        expected_token = None
                        state = None
                    else:
                        if mode:
                            self.__tag_buf__.append((name, tag))
                        else:
                            if tag == TAGS.AND or tag == TAGS.OR:
                                self.__str_buf__ += ' ' + name + ' '
                            else:
                                self.__str_buf__ += name
                elif state == STATES.INPUT:
                    if tag == TAGS.NEXT_CMD:
                        if mode:
                            cmds = self.translate_to_commands(self.to_polska(self.__tag_buf__))
                            self.__append_command__(COMMANDS.WRITE_TO)
                            self.__append_command__(cmds[1:])
                            self.__tag_buf__ = []
                        else:
                            self.__append_command__(self.__str_buf__)
                            self.__str_buf__ = ""
                        expected_token = None
                        state = None
                    else:
                        if mode:
                            self.__tag_buf__.append((name, tag))
                        else:
                            if tag == TAGS.AND or tag == TAGS.OR:
                                self.__str_buf__ += ' ' + name + ' '
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
                    if mode:
                        self.__append_command__(self.get_id_address(name))
                    else:
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

        if mode:
            self.__append_command__(COMMANDS.DONE)
            self.__program__ = self.translate_to_commands(self.__program__)



    __backturns_stack__ = list()

    __cur_cmd__ = 0

    def __append_command__(self, cmd):
        if type(cmd) is list:
            for c in cmd:
                self.__program__.append(c)
                self.__cur_cmd__ += 1
        else:
            self.__program__.append(cmd)
            self.__cur_cmd__ += 1

    def __push_backturn__(self, tag, op0_offset=0):
        self.__backturns_stack__.append((tag, len(self.__program__)-1-op0_offset, len(self.__program__)))

    def __pop_backturn__(self):
        return self.__backturns_stack__.pop()

    def get_program(self):
        return self.__program__


class NotExpected(Exception):
    pass



