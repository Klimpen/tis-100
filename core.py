from constants import *
from instruction_set import *

class Core():

    def __init__(self):
        
        self.program_memory = [Byte()] * 2**11 # set to 1000 for the moment, should put this as less?
        self.program_counter = 0

        self.acc = Byte()
        self.bak = Byte()

        result = None       # TODO: Figure this - placeholder
        self.success = True # DEFAULT = TRUE, reset to True each tick. False = do not increment program_counter; True = increment program_counter

        self.left = None # contains a shared byte
        self.right = Byte() # these bytes are shared registers between adjacent cores
        self.up = Byte()
        self.down = None

    def run(self):        
        Instruction_Set.decode(self, self.program_memory[self.program_counter])

    #TODO: update this to use 'add(pc, imm), 0x1'
    def update_program_counter(self):
        if self.success:
            self.program_counter += 1
            self.program_counter %= 2**11
        else:
            self.success = True