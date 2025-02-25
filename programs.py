
class Programs:

    def fib_gen():
        return [2, 2, "MOV ACC IMM\n 1\n ADD ACC BAK\n ADD BAK ACC\n MOV PC IMM\n 1\n", "ADD ACC IMM\n 1\n MOV PC IMM\n -1", "MOV PC IMM\n 0", "MOV PC IMM\n 0"]