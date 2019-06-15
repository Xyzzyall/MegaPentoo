from MegaPentoo.Lexer.ImpLexer import *
from MegaPentoo.Parser.Parser import *
from MegaPentoo.Interpretator.Interpretator import *


def fancy_out(code):
    i = 0
    for cmd in code:
        print(str(i) + ": " + cmd)
        i += 1


test1 = """
    lookin a
    lookin b
    lookin c
    
    while a > c do
        a = a - c
        b = b + a
        pentoo "TICK" 
    end
    pentoo a
    pentoo b
    pentoo c+1
    
    
"""


t1 = Parser()
t1.analyze_tokens(imp_lex(test1))
prog = t1.get_program()
fancy_out(prog)

print()

inter = Interpretator(prog)
inter.run()
