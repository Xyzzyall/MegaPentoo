


class Interpretator:
    program = list()

    def __init__(self, program):
        self.program = program

    def run(self):
        i = 0
        prog_len = len(self.program)
        op1, op2 = None, None

        exec("condition = 0", globals())

        while i < prog_len:
            current_elem = self.program[i]
            if prog_len - i > 1:
                op1 = self.program[i + 1]
            if prog_len - i > 2:
                op2 = self.program[i + 2]

            if current_elem == "write_to":

                exec(op1 + " = " + op2, globals())
                i = i + 2
            elif current_elem == "write_cond":
                exec("condition = " + op1, globals())
                i = i + 1
            elif current_elem == "goto":
                i = int(op1)-1
            elif current_elem == "print":
                exec("print(" + op1 + ")", globals())
                i = i + 1
            elif current_elem == "cond_goto":
                if eval("condition", globals()):
                    i = int(op1)-1
            elif current_elem == "not_cond_goto":
                if not eval("condition", globals()):
                    i = int(op1)-1
            elif current_elem == "input":
                exec(op1 + "= int(input())", globals())

            i = i + 1

        #print(globals())

proga1 = [
    "input",
    "b",
    "write_cond",
    "b < 100 ",
    "not_cond_goto",
    "13",
    "write_to",
    "b",
    "b + 2",
    "print",
    "b",
    "goto",
    "2"
]

p1 = Interpretator(proga1)
p1.run()
