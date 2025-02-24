from constants import *

class Parse_Program:

    programs = []

    def __init__(self, input):
        
        self.height = CORES_HEIGHT
        self.width = CORES_WIDTH

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

        instruction = self.parse_instruction(words[0])
        dst = self.parse_address(words[1])
        src = self.parse_address(words[2])
        output = Byte(instruction * 256 + dst * 16 + src)
        return output
        
    
    def parse_instruction(self, instruction):

        match(instruction):
            case "MOV": return 0
            case "HAS": return 1
            case "BSL": return 2
            case "CMP": return 3

            case "ADD": return 4
            case "XOR": return 5
            case "JEZ": return 6
            case "JGZ": return 7

            case _: raise Exception("Wrong instruction input")

    def parse_address(self, address):

        match(address):
            case "NIL": return 0
            case "ACC": return 1
            case "BAK": return 2
            case "IMM": return 3

            case "LEFT": return 4
            case "RIGHT": return 5
            case "UP": return 6
            case "DOWN": return 7

            case "ANY": return 8
            case "LAST": return 9
            case "ALL": return 10
            case "IO": return 11

            case "PC": return 12
            case "PM": return 13
            case "MB": return 14
            case "MA": return 15

            case _: raise Exception("Wrong address input")

