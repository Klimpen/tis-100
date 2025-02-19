from constants import *
from instruction_set import *

class Core():

    def __init__(self):

        self.decoder = Decoder(self)
        
        self.program_memory = [Byte(0b00000000000), # test program
                                Byte(0b00100000000),
                                Byte(0b01000000000),
                                Byte(0b01100000000),
                                Byte(0b10000000000),
                                Byte(0b10100000000),
                                Byte(0b11000000000),
                                Byte(0b11100000000)]
        # self.program_memory = [Byte()] * 2**11 # set to 1000 for the moment, should put this as less?
        self.program_counter = 0

        self.acc = Byte(0b0)
        self.bak = Byte(0b0)

        self.result = None      # TODO: Figure this - placeholder
        self.success = True     # DEFAULT = TRUE, reset to True each tick. False = do not increment program_counter; True = increment program_counter

        self.left = None        # contains a bus
        self.right = Bus()      # these bus are shared registers between adjacent cores
        self.up = Bus()
        self.down = None


    def run(self):        
        instruction = self.program_memory[self.program_counter].value
        self.decoder.decode(instruction)

    #TODO: update this to use 'add(pc, imm), 0x1'
    def update_program_counter(self):
        if self.success:
            self.program_counter += 1
            self.program_counter %= 8
        else:
            self.success = True


#   Each instruction is 1 byte
#   [3bit][4bit][4bit]
#   instruction - dst address - src address
class Decoder():

    def __init__(self, core):
        self.core= core

        self.instruction = 0b0
        self.dst = 0b0
        self.src = 0b0


    def decode(self, instruction):

        self.instruction = instruction & 0b11100000000
        self.dst         = instruction & 0b00011110000
        self.src         = instruction & 0b00000001111

        self.run()

    def run(self):
        instruction = self.instruction
        match(instruction):
            case 0b00000000000: Instruction_Set.mov(self.core, self.dst, self.src)
            case 0b00100000000: Instruction_Set.has(self.core, self.dst, self.src)
            case 0b01000000000: Instruction_Set.bsl(self.core, self.dst, self.src)
            case 0b01100000000: Instruction_Set.cmp(self.core, self.dst, self.src)
            case 0b10000000000: Instruction_Set.add(self.core, self.dst, self.src)
            case 0b10100000000: Instruction_Set.xor(self.core, self.dst, self.src)
            case 0b11000000000: Instruction_Set.jez(self.core, self.dst, self.src)
            case 0b11100000000: Instruction_Set.jgz(self.core, self.dst, self.src)