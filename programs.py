
from collections import Enum
from schema import Schema

class Schemas(Enum):
    fib_gen = Schema.from_single_assembly(
        '''
        MOV ACC IMM
        1
        ADD ACC BAK
        ADD BAK ACC
        MOV PC IMM
        1
        '''
    )

    adder = Schema.from_single_assembly(
        '''MOV BAK IMM
        1
        MOV ACC BAK
        ADD ACC BAK
        MOV PC IMM
        2
        '''
    )

    add_and_fib = Schema.from_assembly(
        2, 1,
        [
            '''
            MOV ACC IMM
            1
            ADD ACC BAK
            ADD BAK ACC
            MOV PC IMM
            1
            ''',
            '''
            MOV BAK IMM
            1
            MOV ACC BAK
            ADD ACC BAK
            MOV PC IMM
            2'''
        ]
    )
    
    mutating_test_one = Schema.from_single_assembly(
        '''
        MOV ACC IMM
        1
        ADD MA ACC
        ADD MA ACC
        MOV PM IMM
        ADD ACC BAK
        ADD MA ACC
        MOV PM IMM
        ADD BAK ACC
        ADD MA ACC
        MOV PM IMM
        MOV PC IMM
        ADD MA ACC
        MOV PM IMM
        2
        MOV PC IMM
        0
        '''
    )
