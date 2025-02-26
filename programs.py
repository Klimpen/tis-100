
class Programs:

    def fib_gen():
        return [1, 1, 
            '''MOV ACC IMM
            1
            ADD ACC BAK
            ADD BAK ACC
            MOV PC IMM
            1''']
    
    def adder():
        return [1, 1,
                '''MOV BAK IMM
                1
                MOV ACC BAK
                ADD ACC BAK
                MOV PC IMM
                2''']
    
    def add_and_fib():
        return [2, 1,
                '''MOV ACC IMM
                1
                ADD ACC BAK
                ADD BAK ACC
                MOV PC IMM
                1''',
                '''MOV BAK IMM
                1
                MOV ACC BAK
                ADD ACC BAK
                MOV PC IMM
                2''']