from MegaPentoo.Lexer.ImpLexer import *
from MegaPentoo.Parser.Parser import *


def fancy_out(code):
    i = 0
    for cmd in code:
        print(str(i) + ": " + cmd)
        i += 1


test1 = """
    a = 1 + 1
    if a < 2 then 
        b = 3
        while c < 1 do
            r = 123
        end
    end
    b = 1
    while c > 1 do
        b = b + 1
    end
    pentoo a + b
    lookin c
"""


t1 = Parser()
t1.analyze_tokens(imp_lex(test1))
fancy_out(t1.get_program())
