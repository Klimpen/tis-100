# Specification for TIS-100

## Instruction set

The instruction set is 11-bits. Each is followed by two 4-bit addresses as operands, one for the destination and one for the source.

```
000 MOV [DST][SRC]
001 HAS [DST][SRC]
010 BSL                     # bit shift?
011 CMP [DST][SRC]          # unsure

100 ADD [DST][SRC]
101 XOR [DST][SRC]
110 JEZ [DST][SRC]
111 JGZ [DST][SRC]
```

## Metaprogramming

Macros can compose common reusable functionality out of the basic instructions. The following are some examples of how to compose instructions.

```
NOP =
    MOV [ACC][ACC]

NEG[DST] = 
    XOR [DST][IMM]
     1 11111 11111

SUB[DST][SRC] = 
    #IMPORTANT: SUB[DST][DST] = 0
    NEG[DST]
    ADD[DST][SRC]
    NEG[DST]
```

## Addressable space

The address space is 4 bits. The following addresses are available:

- [DST] = 4bit Address
- [SRC] = 4bit Address

```
0000 NIL
0001 ACC
0010 BAK
0011 IMM EDIATE

0100 LEFT
0101 RIGHT
0110 UP
0111 DOWN

1000 ANY
1001 LAST
1010 ALL
1011 I/O                    # Unsure - isnt I/O just static memory address? Maybe second memtable to do I/O on? Screen: 160 wide x 60 high = 9600 is more addresses than we can handle. Thought required.

1100 PC - PROGRAM COUNTER
1101 PM - PROGRAM MEMORY
1110 MB - MEM BLOCK              # Unsure -  I like this idea but am unsure about execution
1111 MA - MEM ADDRESS
```

## Value representation

Values are stored as 1s complement, 11-bit integers. The most significant bit is the sign bit. The remaining 10 bits are the magnitude of the value.

```
0 _____ _____ NEG FLAG
_ 00000 00000 2^10 BYTE

 0 00000 00000 = +0
 1 11111 11111 = -0
```

---

## Notes

Clocks are shared between all cores.

All computation happens simultaneously.
Then, all `pc` registers are updated simultaneously.
