
class Programs:

    def fib_gen():
        return [1, 1, "MOV ACC IMM\n 1\n ADD ACC BAK\n ADD BAK ACC\n MOV PC IMM\n 1\n"]