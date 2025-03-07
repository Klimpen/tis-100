from constants import *
from instruction_set import *

class Core():

    def __init__(self, memory_program, memory_general, memory_io, read_io):
        
        self.memory_general = memory_general
        self.memory_address = 0

        self.memory_io = memory_io
        self.read_io = read_io

        self.memory_program = memory_program
    
        self.program_counter = 0

        self.acc = Byte(0b0)
        self.bak = Byte(0b0)

        self.result = None      # TODO: Figure this - placeholder
        self.success = True     # DEFAULT = TRUE, reset to True each tick. False = do not increment program_counter; True = increment program_counter


        self.left = None        # contains a bus
        self.right = Bus()      # these bus are shared registers between adjacent cores
        self.up = Bus()
        self.down = None

        self.last_left = False
        self.last_right = False
        self.last_up = False
        self.last_down = False

        self.curr_left = False
        self.curr_right = False
        self.curr_up = False
        self.curr_down = False

    def has_value(self, address):
        match(address):
            case 0b0100: return self.left.send
            case 0b0101: return self.right.send
            case 0b0110: return self.up.send
            case 0b0111: return self.down.send

            case 0b1000: return self.has_any()
            case 0b1001: return self.has_last()
            case 0b1010: return self.has_all()
            case _: Exception(address)

    def has_any(self):
        return (
            self.left.send or 
            self.right.send or 
            self. up.send or 
            self.down.send)

    def has_last(self):
        return (
            (self.left.send and self.last_left) or
            (self.right.send and self.last_right) or
            (self.up.send and self.last_up) or
            (self.down.send and self.last_down))

    def has_all(self):
        return (
            self.left.send and
            self.right.send and 
            self. up.send and
            self.down.send)

    def get_value(self, address):
        
        match(address):
            case 0b0000: return 0b0 
            case 0b0001: return self.acc.value
            case 0b0010: return self.bak.value
            case 0b0011: return self.get_immediate()

            case 0b0100: return self.get_direction(self.left)
            case 0b0101: return self.get_direction(self.right)
            case 0b0110: return self.get_direction(self.up)
            case 0b0111: return self.get_direction(self.down)

            case 0b1000: return self.get_any()
            case 0b1001: return self.get_last()
            case 0b1010: raise Exception("Cannot read from ALL") # cannot read from ALL
            case 0b1011: return self.read_io

            case 0b1100: return self.program_counter
            case 0b1101: return self.get_memory(self.memory_program)
            case 0b1110: return self.memory_address
            case 0b1111: return self.get_memory(self.memory_general)
            case _: raise Exception(address)

    def get_immediate(self):
            self.program_counter += 1
            self.program_counter %= len(self.memory_program)

            return self.memory_program[self.program_counter].value

    def get_direction(self, direction):
        value = direction.read()

        if value is None:
            self.success = False

        return value

    def get_any(self):
        # case: there is something to get
        output = None

        if self.has_any():
            if self.left.send: output = self.get_direction(self.left)
            if self.right.send: output = self.get_direction(self.right)
            if self.up.send: output = self.get_direction(self.up)
            if self.down.send: output = self.get_direction(self.down)
            return output
        
        # case: there is not something to get
        self.success = False
        return output

    def get_last(self):
        output = None

        if self.has_last(self):
            if self.left.send and self.last_left: self.get_direction(self.left)
            if self.right.send and self.last_right: self.get_direction(self.right)
            if self.up.send and self.last_up: self.get_direction(self.up)
            if self.down.send and self.last_down: self.get_direction(self.down)
            return output
            

    def get_memory(self, memory):
        return memory[self.memory_address].value
    
    def write_value(self, address, value):

        checked_vaLue = self.bounds_check(value)

        match(address):
            case 0b0000 : pass
            case 0b0001 : self.acc.value = checked_vaLue
            case 0b0010 : self.bak.value = checked_vaLue
            case 0b0011 : self.write_immediate(checked_vaLue)

            case 0b0100 : self.write_direction(self.left, checked_vaLue)
            case 0b0101 : self.write_direction(self.right, checked_vaLue)
            case 0b0110 : self.write_direction(self.up, checked_vaLue)
            case 0b0111 : self.write_direction(self.down, checked_vaLue)

            case 0b1000 : self.write_any(checked_vaLue)
            case 0b1001 : self.write_last(checked_vaLue)
            case 0b1010 : self.write_all(checked_vaLue)
            case 0b1011 : self.write_memory(value, self.memory_io) 

            case 0b1100 : self.write_pc(checked_vaLue)
            case 0b1101 : self.write_memory(value, self.memory_program)
            case 0b1110 : self.memory_address = checked_vaLue
            case 0b1111 : self.write_memory(value, self.memory_general)
            case _: raise Exception(address)
    
    def bounds_check(self, value):
        if value > 1024:
            value -= 2048
        if value < -1024:
            value += 2048
        return value
    
    def write_immediate(self, value):
        self.memory_program[self.program_counter+1].value = value

    def write_direction(self, direction, value):
        self.success = direction.write(value)

    def write_any(self, value):
        pass

    def write_last(self, value):
        pass

    def write_all(self, value):
        pass

    def write_pc(self, value):
        self.program_counter = value
        self.success = False

    def write_memory(self, value, memory):
        memory[self.memory_address].value = value

    def run(self):        
        instruction = self.memory_program[self.program_counter].value
        self.decode(instruction)

    #TODO: update this to use 'add(pc, 0b1)'
    def update(self):
        if self.success:
            self.program_counter += 1
            self.program_counter %= len(self.memory_program)
        else:
            self.success = True

        self.last_left = self.curr_left
        self.last_right = self.curr_right
        self.last_up = self.curr_up
        self.last_down = self.curr_down


#   Each instruction is 1 byte
#   [3bit][4bit][4bit]
#   instruction - dst address - src address
    def decode(self, value):

        
        instruction = (value >> 8)
        dst         = (value >> 4) & 0b0001111
        src         = (value & 0b00000001111)
        
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