from MegaPentoo.Lexer.ImpLexer import *
from MegaPentoo.Parser.Parser import *
from MegaPentoo.VM.VM import *

def fancy_out(code):
    i = 0
    for cmd in code:
        print(str(i) + ": " + str(cmd))
        i += 1

test = [
"""
lookin len
i = 2
prev = 1
prev2 = 1
next = 0
pentoo 1
pentoo 1

while i < len do
    next = prev + prev2
    prev2 = prev
    prev = next
    pentoo next 
    i = i + 1
end 
""",
"""
lookin a
lookin b
lookin c

if a < b and b < c then
    pentoo 1
end
""",
"""
lookin a
res = 1
while a > 1 do
    res = a * res
    a = a - 1
end
pentoo res
""",
"""
lookin a
lookin b

c = a - b
if c == 10 then
    pentoo 10
end

if a > b then
    pentoo a
end

if a < b then
    pentoo b
end

i = 0
j = 0

while i < a do
     i = i + 1
     while j < b do
        j = j + 1
        pentoo i*1000 + j
     end
     j = 0
end
"""]

t1 = Parser()
t1.analyze_tokens(imp_lex(test[3]))
prog = t1.get_program()
fancy_out(prog)

vm = VM(prog)
vm.run()
