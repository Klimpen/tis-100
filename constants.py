
from enum import Enum
from typing import Tuple

# INSTRUCTIONS
class Instruction(Enum):
    '''
    Instructions are 3 bits long, and are packed into the most significant bits of a byte.

    These represent the operations that the core can perform.
    '''
    MOV = 0b000
    '''Copy the value from the source register to the destination register.'''
    HAS = 0b001
    '''Check if there is a value to read from the source register.'''
    BSL = 0b010
    '''Bitwise shift left.'''
    CMP = 0b011
    '''Compare the value in the source register to the value in the destination register.'''

    ADD = 0b100
    '''Add the value in the source register to the value in the destination register.'''
    XOR = 0b101
    '''Bitwise XOR the value in the source register with the value in the destination register.'''
    JEZ = 0b110
    '''Jump to the address in the destination register if the value in the source register is zero.'''
    JGZ = 0b111
    '''Jump to the address in the destination register if the value in the source register is greater than zero.'''

# ADDRESSABLE SPACE
class Register(Enum):
    '''
    Registers are 4 bits long, and are packed into the least significant bits of a byte.

    These represent the different types of memory that the core can access, or perform special hardware tasks.
    '''
    NIL   = 0b0000
    ACC   = 0b0001
    BAK   = 0b0010
    IMM   = 0b0011 # immediate = next byte

    LEFT  = 0b0100
    RIGHT = 0b0101
    UP    = 0b0110
    DOWN  = 0b0111

    ANY   = 0b1000
    LAST  = 0b1001
    ALL   = 0b1010
    IO    = 0b1011

    PC    = 0b1100 # program counter
    PM    = 0b1101 # program memory
    MA    = 0b1110 # memory address - used to read/write io/program/general memory
    MEM   = 0b1111 # general memory

# A byte is 11 bits in this architecture
class Byte():
    __slots__ = ['value']
    instruction_shift = 8
    instruction_mask = 0b111
    destination_shift = 4
    source_shift = 0
    register_mask = 0b1111
    def __init__(self, value: int):
        self.value = value

    @classmethod
    def pack(self, inst: Instruction, dst: Register, src: Register) -> 'Byte':
        '''
        Return a new byte with the given instruction, destination, and source packed into it.
        '''
        return Byte(
            (inst << self.instruction_shift) |
            (dst << self.destination_shift) |
            (src << self.source_shift)
        )

    def unpack(self) -> Tuple[Instruction, Register, Register]:
        '''
        Return the instruction, destination, and source components packed into this byte.
        '''
        return (
            Instruction((self.value >> self.instruction_shift) & self.instruction_mask),
            Register((self.value >> self.destination_shift) & self.register_mask),
            Register((self.value >> self.source_shift) & self.register_mask),
        )

# XXX: This doesn't seem like it belongs in constants, and the name is a bit odd. Maybe Link would be more appropriate?
class Bus():
    value = None
    send = False

    def get(self):
        # case - there is soemthing to read from bus
        if self.send:
            self.send = False

        # always return - value if there is one, none otherwise. core.read handles return values
        return self.value


    def write(self, value):

        # case - writing to bus
        if self.value is None:
            self.value = value
            self.send = True
            return False
        
        # case - waiting for bus to be read
        if self.send is not None:
            return False
        
        # case - bus read - wiping bus
        value = None
        return True

