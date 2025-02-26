
# INSTRUCTIONS
MOV = 0b000
HAS = 0b001
BSL = 0b010 
CMP = 0b011

ADD = 0b100
XOR = 0b101
JEZ = 0b110
JGZ = 0b111

# ADDRESSABLE SPACE
NIL   = 0b0000
ACC   = 0b0001
BAK   = 0b0010
IMM   = 0b0011 #immediate = next byte

LEFT  = 0b0100
RIGHT = 0b0101
UP    = 0b0110
DOWN  = 0b0111

ANY   = 0b1000
LAST  = 0b1001
ALL   = 0b1010
IO    = 0b1011 

PC    = 0b1100 #program counter
PM    = 0b1101 #program memory
MA    = 0b1110 #memory address - used to read/write io/program/general memory
MEM    = 0b1111 #general memory

# A byte is 11 bits in this architecture
class Byte():

    def __init__(self, value):
        self.value = value

class Bus():
    value = None
    send = False

    def get(self):
        # case - there is soemthing to read from bus
        if self.send:
            self.send = False

        # always return - value if there is one, none otherwise. core.read handles return values
        return self.value


    def write(self, value):

        # case - writing to bus
        if self.value is None:
            self.value = value
            self.send = True
            return False
        
        # case - waiting for bus to be read
        if self.send is not None:
            return False
        
        # case - bus read - wiping bus
        value = None
        return True

