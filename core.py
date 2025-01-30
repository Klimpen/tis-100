from main import *
from instruction_set import *

class Core():

    def __init__(self):
        
        self.program_memory = [1000] # set to 1000 for the moment, should put this as less?
        self.program_counter = 0

        self.acc = 0
        self.bak = 0

        self.result = None # set to None at the end of each instruction
        self.success = True # DEFAULT = TRUE, reset to True each tick. False = do not increment program_counter; True = increment program_counter

        self.left = None # containts a reference to another core - is this the best way to do this? 
        self.right = None # would it make more sense to have a different object which can handle the transmission of data core-core?
        self.up = None
        self.down = None

    def run(self):        
        instruction_set.decode(self, self.program_memory[self.program_counter])

    #TODO: update this to use add()
    def update(self):
        if self.success:
            self.program_counter += 1
        else:
            self.success = True