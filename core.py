from constants import *
from instruction_set import *

class Core():

    def __init__(self, memory_general, memory_io):
        
        self.memory_general = memory_general
        self.memory_io = memory_io
        self.memory_program = [ Byte(0b00000010011), # MOV ACC IMM
                                Byte(0b00000000001), # 1
                                Byte(0b10000010010), # ADD ACC BAK
                                Byte(0b10000100001), # ADD BAK ACC
                                Byte(0b00011000011), # JMP PC IMM
                                Byte(0b00000000001), # 0
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),
                                Byte(0b00000000000),]
        
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
        pass

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
            case 0b1011: return self.get_memory(self.memory_io)

            case 0b1100: return self.program_counter
            case 0b1101: return self.get_memory(self.memory_program)
            case 0b1110: pass # read block from general memory
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
        pass

    def get_memory(self, memory):
        return memory[self.get_immediate()].value
    
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
            case 0b1011 : self.write_memory(value, self.memory_io) 

            case 0b1100 : self.program_counter = value
            case 0b1101 : self.write_memory(value, self.memory_program)
            case 0b1110 : pass # write block from general memory
            case 0b1111 : self.write_memory(value, self.memory_general)
            case _: raise Exception(address)

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

    def write_memory(self, value, memory):
        memory[self.get_immediate()].value = value

    def run(self):        
        instruction = self.memory_program[self.program_counter].value
        self.decode(instruction)

    #TODO: update this to use 'add(pc, 0b1)'
    def update_program_counter(self):
        if self.success:
            self.program_counter += 1
            self.program_counter %= len(self.memory_program)
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


    def draw(self):
        output = []
        output.append(".----------------------.")
        for i in range(0,16):
            if i == self.program_counter:
                output.append(f"| \033[7m{self.draw_decode(self.memory_program[i].value)}\033[27m |")
            else:
                output.append(f"| {self.draw_decode(self.memory_program[i].value)} |")
        output.append("*----------------------*")

        output[0] += f"------."
        output[1] += f"  PC  |"
        output[2] += f"{f" {self.program_counter} |":>7}"
        output[3] += f"------*"
        output[4] += f"  ACC |"
        output[5] += f"{f" {self.acc.value} |":>7}"
        output[6] += f"------*"
        output[7] += f"  BAK |"
        output[8] += f"{f" {self.bak.value} |":>7}"
        output[9] += f"------*"
        output[10] += f"RESULT|"
        output[11] += f"{f" {self.result} |":>7}"
        output[12] += f"------*"
        output[13] += f" LAST |"
        output[14] += f"{f"  |":>7}"
        output[15] += f"------*"
        output[16] += f"      |"
        output[17] += f"------*"

        return output

    def draw_decode(self, byte):
        
        instruction = (byte & 0b11100000000) // 256
        dst         = (byte & 0b00011110000) // 16
        src         = (byte & 0b00000001111)

        instruction_name = self.name_instruction(instruction)
        dst_name = self.name_address(dst)
        src_name = self.name_address(src)

        output = f"{instruction_name} {dst_name} {src_name}"
        if output == "MOV NIL NIL":
            output = ""
        return f"{f"{output}":<20}"

    def name_instruction(self, instruction):
        match(instruction):
            case 0b000: return "MOV"
            case 0b001: return "HAS"
            case 0b010: return "BSL"
            case 0b011: return "CMP"
            
            case 0b100: return "ADD"
            case 0b101: return "XOR"
            case 0b110: return "JEZ"
            case 0b111: return "JGZ"

    def name_address(self, address):
        match(address):
            case 0b0000: return "NIL"
            case 0b0001: return "ACC"
            case 0b0010: return "BAK"
            case 0b0011: return "IMM"
            
            case 0b0100: return "LEFT"
            case 0b0101: return "RIGHT"
            case 0b0110: return "UP"
            case 0b0111: return "DOWN"
            
            case 0b1000: return "ANY"
            case 0b1001: return "LAST"
            case 0b1010: return "ALL"
            case 0b1011: return "IO"
            
            case 0b1100: return "PC"
            case 0b1101: return "PM"
            case 0b1110: return "MB"
            case 0b1111: return "MA"
