
# INSTRUCTIONS
MOV = 0b000
HAS = 0b001
BSL = 0b010 # UNSURE - BIT SHIFT LEFT?
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
DOW   = 0b0111

ANY   = 0b1000
LAST  = 0b1001
ALL   = 0b1010
IO    = 0b1011 # UNSURE - ADDRESSABLE MEMORY IS SMALLER THAN SCREEN [160x60 char]

PC    = 0b1100 #program counter
PM    = 0b1101 #program memory
MB    = 0b1110 #memory block
MA    = 0b1111 #memory address

# VALUES

CORES_WIDTH = 2
CORES_HEIGHT = 2

# A byte is 11 bits in this architecture
class Byte():

    def __init__(self, value):
        self.value = value

class Bus():
    value = None
    send = False
    receive = False

    def get(self):
        pass

    def write(self, value):
        pass