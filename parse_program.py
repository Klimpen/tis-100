from constants import *

class Parse_Program:

    programs = []

    def __init__(self, input):

        for program in input:
            self.programs.append(self.parse_core(program))

    def parse_core(self, program_string):
        output = []
        for line in program_string.splitlines():
            output.append(self.parse_line(line))
        return output
    
    def parse_line(self, line):

        words = line.split()
        if len(words) == 1:
            output = Byte(int(words[0]))
            return output

        instruction = self.parse_instruction(words[0]) << 8
        dst = self.parse_address(words[1]) << 4
        src = self.parse_address(words[2])
        output = Byte(instruction + dst + src)
        return output
        
    
    def parse_instruction(self, instruction):

        match(instruction):
            case "MOV": return 0b000
            case "HAS": return 0b001
            case "BSL": return 0b010
            case "CMP": return 0b011

            case "ADD": return 0b100
            case "XOR": return 0b101
            case "JEZ": return 0b110
            case "JGZ": return 0b111

            case _: raise Exception("Wrong instruction input")

    def parse_address(self, address):
        match(address):
            case "NIL": return NIL
            case "ACC": return ACC
            case "BAK": return BAK
            case "IMM": return IMM

            case "LEFT": return LEFT
            case "RIGHT": return RIGHT
            case "UP": return UP
            case "DOWN": return DOWN

            case "ANY": return ANY
            case "LAST": return LAST
            case "ALL": return ALL
            case "IO": return IO

            case "PC": return PC
            case "PM": return PM
            case "MA": return MA
            case "MEM": return MEM

            case _: raise Exception("Wrong address input")

