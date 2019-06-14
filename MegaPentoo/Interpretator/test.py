from . import *

proga1 = [
    "write_to",
    "a",
    "3"
    "write_cond",
    " a > 0 ",
    "cond_goto",
    "12",
    "write_to",
    "b",
    "b + 1",
    "goto",
    "0",
    "print",
    "b"
]

p1 = Interpretator(proga1)
p1.run()
