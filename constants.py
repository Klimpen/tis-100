# INSTRUCTIONS

MOV = 0x000
HAS = 0x001
BSL = 0x010 # UNSURE - BIT SHIFT LEFT?
CMP = 0x011 # COMPARE

ADD = 0x100
XOR = 0x110
JEZ = 0x110
JGZ = 0x111

# ADDRESSABLE SPACE

NIL = 0x0000
ACC = 0x0001
BAK = 0x0010
IMM = 0x0011 #immediate = next byte

LEF = 0x0100
RIG = 0x0101
UP  = 0x0110
DOW = 0x0111

ANY = 0x1000
LAS = 0x1001
ALL = 0x1010
IO  = 0x1011 # UNSURE - ADDRESSABLE MEMORY IS SMALLER THAN SCREEN [160x60 char]

PC  = 0x1100 #program counter
PM  = 0x1101 #program memory
MB  = 0x1110 #memory block
MA  = 0x1111 #memory address

# VALUES

CORES_WIDTH = 6
CORES_HEIGHT = 4

# STRUCTS
# A byte is 11 bits in this architecture
# Each instruction is 1 byte
#   [3bit][4bit][4bit]
#   instruction - dst address - src address

class Byte():
    value = None