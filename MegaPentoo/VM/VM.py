from enum import Enum


class COMMANDS(Enum):
    WRITE_TO = 0
    GOTO = 1
    GOTO_CONDITION = 2
    COND_LESS = 3
    COND_MORE = 4
    COND_EQUAL = 5
    COND_NOT_EQUAL = 6
    COND_AND = 7
    COND_OR = 8
    PLUS = 9
    MINUS = 10
    MULT = 11
    DIVIDE = 12
    PUSH = 13  # push constant to stack
    POP = 14
    PRINT = 15
    INPUT = 16
    GOTO_NOT_CONDITION = 17
    DONE = 18   # writes result to target
    PUSH_VAR = 19  # push variable to stack
    DIRECT = 20  # direct python run
    COND_RESET = 21 # reset condition to false
    WRITE_TO_CONDITION = 22
    PUSH_FLAG_NEG = 23
    PUSH_FLAG_POS = 24
    PUSH_FLAG_ZERO = 25
    PUSH_FLAG_NOT_ZERO = 26


MEMORY = 8


class VM:
    __commands__ = [
        "write_to",
    ]

    __program__ = list()

    def __init__(self, program):
        self.__program__ = program

    __stack__ = list()

    def __push__(self, elem):
        self.__stack__.append(elem)

    def __pop__(self):
        return self.__stack__.pop()

    #            zero   neg
    __flags__ = [False, False]

    def __upd_flags__(self, num):
        if num == 0:
            self.__flags__[0] = True
        else:
            self.__flags__[0] = False

        if num < 0:
            self.__flags__[1] = True
        else:
            self.__flags__[1] = False

    def run(self, stop=10000000):
        counter = 0
        op1 = None
        op2 = None
        cmd = None
        write_to = COMMANDS.DONE
        memory = [0 for i in range(MEMORY)] # 0 -- condition
        prog_len = len(self.__program__)

        while stop > 0:
            cmd = self.__program__[counter]
            if prog_len - counter > 1:
                op1 = self.__program__[counter + 1]
            if prog_len - counter > 2:
                op2 = self.__program__[counter + 2]

            if cmd == COMMANDS.WRITE_TO:
                write_to = int(op1)
            elif cmd == COMMANDS.GOTO:
                counter = int(op1)-1
            elif cmd == COMMANDS.GOTO_CONDITION:
                if memory[0]:
                    counter = int(op1)-1
                else:
                    counter += 1
            elif cmd == COMMANDS.COND_LESS:
                pass
            elif cmd == COMMANDS.COND_MORE:
                pass
            elif cmd == COMMANDS.COND_EQUAL:
                pass
            elif cmd == COMMANDS.COND_NOT_EQUAL:
                pass
            elif cmd == COMMANDS.COND_AND:
                arg1 = self.__pop__()
                arg2 = self.__pop__()
                res = arg1 and arg2
                self.__push__(res)
            elif cmd == COMMANDS.COND_OR:
                arg1 = self.__pop__()
                arg2 = self.__pop__()
                res = arg1 or arg2
                self.__push__(res)
            elif cmd == COMMANDS.PLUS:
                arg1 = self.__pop__()
                arg2 = self.__pop__()
                res = arg1 + arg2
                self.__upd_flags__(res)
                self.__push__(res)
            elif cmd == COMMANDS.MINUS:
                arg2 = self.__pop__()
                arg1 = self.__pop__()
                res = arg1 - arg2
                self.__upd_flags__(res)
                self.__push__(res)
            elif cmd == COMMANDS.MULT:
                arg1 = self.__pop__()
                arg2 = self.__pop__()
                res = arg1 * arg2
                self.__upd_flags__(res)
                self.__push__(res)
            elif cmd == COMMANDS.DIVIDE:
                arg2 = self.__pop__()
                arg1 = self.__pop__()
                res = arg1 / arg2
                self.__upd_flags__(res)
                self.__push__(res)
            elif cmd == COMMANDS.PUSH:
                self.__push__(int(op1))
                counter += 1
            elif cmd == COMMANDS.POP:
                self.__pop__()
            elif cmd == COMMANDS.PRINT:
                write_to = COMMANDS.PRINT
            elif cmd == COMMANDS.INPUT:
                self.__push__(int(input()))
            elif cmd == COMMANDS.GOTO_NOT_CONDITION:
                if not memory[0]:
                    counter = int(op1) - 1
                else:
                    counter += 1
            elif cmd == COMMANDS.DONE:
                if write_to != COMMANDS.DONE:
                    if type(write_to) is COMMANDS:
                        if write_to == COMMANDS.PRINT:
                            print(self.__pop__())
                    else:
                        memory[write_to] = self.__pop__()
                else:
                    break
                write_to = COMMANDS.DONE
            elif cmd == COMMANDS.PUSH_VAR:
                self.__push__(memory[op1])
                counter += 1
            elif cmd == COMMANDS.DIRECT:
                pass
            elif cmd == COMMANDS.COND_RESET:
                memory[0] = False
            elif cmd == COMMANDS.WRITE_TO_CONDITION:
                write_to = 0
            elif cmd == COMMANDS.PUSH_FLAG_NEG:
                self.__push__(self.__flags__[1])
            elif cmd == COMMANDS.PUSH_FLAG_POS:
                self.__push__(not self.__flags__[1])
            elif cmd == COMMANDS.PUSH_FLAG_ZERO:
                self.__push__(self.__flags__[0])
            elif cmd == COMMANDS.PUSH_FLAG_NOT_ZERO:
                self.__push__(not self.__flags__[0])

            counter += 1
            stop -= 1




    pass