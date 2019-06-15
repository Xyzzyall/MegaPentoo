from MegaPentoo.Lexer.Lexer import *
from MegaPentoo.Lexer.Tokens import *

tests = [
    """
   // Hello, my little pidor. Today we'll programm your ass!
    
    proga Chika()
        for i = 1 to 5
            begin
            pentoo("proga Chika is running")
            a = i + 4
            c = i - 2
            end 
        return a 
    
    d = 2*2
    e = 36/6
    if d < 7 and e < 7
        pentoo("< 7")
    if d <= 7 or e <= 7
        pentoo("<= 7")
    if d > 0 and e > 0
        pentoo("> 0")
    if d >= 2 or e >= 0
        pentoo(">= 0")
    
    y = true
    f = false
    t = not f
    pentoo(y, f, t)
    if t == f
        pentoo("logica is ok")
    
    pentoo("Please suck, or input a count bigger than zero")    
    lookin(task)
    while task not== 0
        begin 
        pentoo("DICK")
        task = task - 1
        end    
    """,
    """
    lookin a
    if a > 3 then 
        print(a)
    end
    """
]

lx = Lexer()
print(lx.lex(tests[1], token_exprs))
