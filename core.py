from constants import *
from instruction_set import *

class Core():

    def __init__(self):

        self.decoder = Decoder(self)
        
        self.program_memory = [Byte()] * 2**11 # set to 1000 for the moment, should put this as less?
        self.program_counter = Byte()

        self.acc = Byte()
        self.bak = Byte()

        self.result = None      # TODO: Figure this - placeholder
        self.success = True     # DEFAULT = TRUE, reset to True each tick. False = do not increment program_counter; True = increment program_counter

        self.left = None        # contains a bus
        self.right = Bus()      # these bus are shared registers between adjacent cores
        self.up = Bus()
        self.down = None


    def run(self):        
        instruction = self.program_memory[self.program_counter]
        self.decoder.decode(instruction)

    #TODO: update this to use 'add(pc, imm), 0x1'
    def update_program_counter(self):
        if self.success:
            self.program_counter.value += 1
            self.program_counter.value %= 2**11
        else:
            self.success = True


#   Each instruction is 1 byte
#   [3bit][4bit][4bit]
#   instruction - dst address - src address
class Decoder():

    def __init__(self, core):
        self.core= core

        self.instruction = None
        self.dst = None
        self.src = None


    def decode(self, instruction):
        self.instruction = instruction & 0b11100000000
        self.dst         = instruction & 0b00011110000
        self.src         = instruction & 0b00000001111

        self.run()

    def run(self):
        match(self.instruction):
            case Instruction.MOV: Instruction_Set.mov(self.core, self.dst, self.src)
            case Instruction.HAS: Instruction_Set.has(self.core, self.dst, self.src)
            case Instruction.BSL: Instruction_Set.bsl(self.core, self.dst, self.src)
            case Instruction.CMP: Instruction_Set.cmp(self.core, self.dst, self.src)
            case Instruction.ADD: Instruction_Set.add(self.core, self.dst, self.src)
            case Instruction.XOR: Instruction_Set.xor(self.core, self.dst, self.src)
            case Instruction.JEZ: Instruction_Set.jez(self.core, self.dst, self.src)
            case Instruction.JGZ: Instruction_Set.jgz(self.core, self.dst, self.src)