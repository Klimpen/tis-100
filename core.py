from constants import *
from instruction_set import *

class Core():

    def __init__(self):
        
        self.program_memory = [Byte(0b00000010001), # test program
                                Byte(0b00100010001),
                                Byte(0b01000010001),
                                Byte(0b01100010001),
                                Byte(0b10000010001),
                                Byte(0b10100010001),
                                Byte(0b11000010001),
                                Byte(0b11100010001)]
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

    def get_value(self, address):

        match(address):
            case Address.NIL: pass # NIL
            case Address.ACC: return self.acc.value
            case Address.BAK: return self.bak.value
            case Address.IMM: return self.get_immediate()

            case Address.LEFT: return self.get_direction(self.left)
            case Address.RIGHT: return self.get_direction(self.right)
            case Address.UP: return self.get_direction(self.up)
            case Address.DOWN: return self.get_direction(self.down)

            case Address.ANY: return self.get_any()
            case Address.LAST: return self.get_last()
            case Address.ALL: raise Exception() # cannot read from ALL
            case Address.IO: pass # read from IO memory 

            case Address.PC: return self.program_counter
            case Address.PM: pass # read from program memory
            case Address.MB: pass # read block from general memory
            case Address.MA: pass # read value from general memory
            case _: raise Exception(address)

    def get_immediate(self):
            self.program_counter += 1
            self.program_counter %= 8

            return self.program_memory[self.program_counter].value

    def get_direction(self, direction):
        value = direction.read()

        if value is None:
            self.success = False

        return value

    def get_any(self):
        pass

    def get_last(self):
        pass

    def write_value(self, address, value):
        match(address):
            case Address.NIL  : pass
            case Address.ACC  : self.acc.value = value
            case Address.BAK  : self.bak.value = value
            case Address.IMM  : self.write_immediate(value)

            case Address.LEFT : self.write_direction(self.left, value)
            case Address.RIGHT: self.write_direction(self.right, value)
            case Address.UP   : self.write_direction(self.up, value)
            case Address.DOWN : self.write_direction(self.down, value)

            case Address.ANY  : self.write_any(value)
            case Address.LAST : self.write_last(value)
            case Address.ALL  : self.write_all(value)
            case Address.IO   : pass # write from IO memory 

            case Address.PC   : self.program_counter = value
            case Address.PM   : pass # write from program memory
            case Address.MB   : pass # write block from general memory
            case Address.MA   : pass # write value from general memory
            case _: raise Exception(address)

    def write_immediate(self, value):
        self.program_memory[self.program_counter+1].value = value

    def write_direction(self, direction, value):
        self.success = direction.write(value)

    def write_any(self, value):
        pass

    def write_last(self, value):
        pass

    def write_all(self, value):
        pass


    def run(self):        
        instruction = self.program_memory[self.program_counter].value
        self.decode(instruction)

    #TODO: update this to use 'add(pc, imm), 0b1'
    def update_program_counter(self):
        if self.success:
            self.program_counter += 1
            self.program_counter %= 8
        else:
            self.success = True


#   Each instruction is 1 byte
#   [3bit][4bit][4bit]
#   instruction - dst address - src address
    def decode(self, byte):

        instruction = (byte & 0b11100000000) // 256
        dst         = (byte & 0b00011110000) // 16
        src         = (byte & 0b00000001111)

        match(instruction):
            case Instruction.MOV: Instruction_Set.mov(self, dst, src)
            case Instruction.HAS: Instruction_Set.has(self, dst, src)
            case Instruction.BSL: Instruction_Set.bsl(self, dst, src)
            case Instruction.CMP: Instruction_Set.cmp(self, dst, src)
            case Instruction.ADD: Instruction_Set.add(self, dst, src)
            case Instruction.XOR: Instruction_Set.xor(self, dst, src)
            case Instruction.JEZ: Instruction_Set.jez(self, dst, src)
            case Instruction.JGZ: Instruction_Set.jgz(self, dst, src)
            case _: raise Exception(instruction)