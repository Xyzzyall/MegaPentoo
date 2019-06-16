from MegaPentoo.Lexer.ImpLexer import *
from MegaPentoo.Parser.Parser import *
from MegaPentoo.VM.VM import *
import sys


def fancy_out(code):
    i = 0
    for cmd in code:
        print(str(i) + ": " + str(cmd))
        i += 1


f = open(sys.argv[1])
p = f.read()

parser = Parser()
parser.analyze_tokens(imp_lex(p))
prog = parser.get_program()

fancy_out(prog)
print("\n\n\n\n\n\n")
inter = VM(prog)
inter.run()

input("Program ended. Press any key.")

