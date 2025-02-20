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
            case 0b0000: pass # NIL
            case 0b0001: return self.acc.value
            case 0b0010: return self.bak.value
            case 0b0011: return self.get_immediate()

            case 0b0100: return self.get_direction(self.left)
            case 0b0101: return self.get_direction(self.right)
            case 0b0110: return self.get_direction(self.up)
            case 0b0111: return self.get_direction(self.down)

            case 0b1000: return self.get_any()
            case 0b1001: return self.get_last()
            case 0b1010: raise Exception() # cannot read from ALL
            case 0b1011: pass # read from IO memory 

            case 0b1100: return self.program_counter
            case 0b1101: pass # read from program memory
            case 0b1110: pass # read block from general memory
            case 0b1111: pass # read value from general memory
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
            case 0b0000 : pass
            case 0b0001 : self.acc.value = value
            case 0b0010 : self.bak.value = value
            case 0b0011 : self.write_immediate(value)

            case 0b0100 : self.write_direction(self.left, value)
            case 0b0101 : self.write_direction(self.right, value)
            case 0b0110 : self.write_direction(self.up, value)
            case 0b0111 : self.write_direction(self.down, value)

            case 0b1000 : self.write_any(value)
            case 0b1001 : self.write_last(value)
            case 0b1010 : self.write_all(value)
            case 0b1011 : pass # write from IO memory 

            case 0b1100 : self.program_counter = value
            case 0b1101 : pass # write from program memory
            case 0b1110 : pass # write block from general memory
            case 0b1111 : pass # write value from general memory
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
            case 0b000: Instruction_Set.mov(self, dst, src)
            case 0b001: Instruction_Set.has(self, dst, src)
            case 0b010: Instruction_Set.bsl(self, dst, src)
            case 0b011: Instruction_Set.cmp(self, dst, src)
            case 0b100: Instruction_Set.add(self, dst, src)
            case 0b101: Instruction_Set.xor(self, dst, src)
            case 0b110: Instruction_Set.jez(self, dst, src)
            case 0b111: Instruction_Set.jgz(self, dst, src)
            case _: raise Exception(instruction)