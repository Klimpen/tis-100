# Specification for TIS-100 inspired architecture

## Overview

This is a specification for a TIS-100 inspired architecture. The architecture is a 2D grid of cores.
Each core has connections to four adjacent cores with connections wrapping around like a torus.

Each core has its own set of registers and memory, a bus shared with each adjacent core for inter-core communication and a bus to the memory controller:

- 2 general purpose registers: `ACC`, and `BAK`.
- 4 I/O mapped bus for directional communication: `LEFT`, `RIGHT`, `UP`, `DOWN`
- 3 I/O mapped bus aliases: `ANY`, `LAST`, and `ALL`.
    `ANY` refers to at least one of the directional commonuication bus.
    `LAST` refers to the last used direction bus(es).
    `ALL` refers to all 4 directional buses.
        This may not be a good idea and requires further thought.
- 1 special-meaning registers: `PC`.
    `PC` is a pointer to the current byte being executed.
    `PC` is incremented every time an instruction successfully executes.
- 1 special-meaning value: `NIL`.
- 1 special meaning alias: `IMM`.
    see below on Literals
- 3 addresses, which instruct the memeory controller 
    `MA` reads/writes to the address of the value passed in the general memory block
    `MB` reads a sequence of values beginning at the first value passed and continuing for a second value number of bytes
    `IO` reads/writes to the address of the value passed in the IO memory block
- 1 address, which interact with the core's program memeory 
    `PM` reads/writes to the address of the value passed in the core program memory

All cores execute exactly one instruction in a cycle, simultaneously.

## Instruction set

The instruction set is 11-bits. The first 3 bits represents the operator, followed by two 4-bit addresses as operands,
one for the destination `[DST]`, then one for the source `[SRC]`. All operators have exactly two operands.

### 000 MOV

`MOV [DST][SRC]` copies the value from the source register to the destination register.

### 001 HAS

`HAS [DST][SRC]` checks if there is a value available to read from an adjacent Core in the direction specified by `[SRC]`.

It is an error to provide a register other than `UP`, `DOWN`, `LEFT`, `RIGHT`, `ANY`, `ALL`, or `LAST` as the source.

The result is written to a temporary register whose result is:
- Usable in the next cycle.
- Then cleared.

- This temporary register is shared with CMP
- 1 if a value is immediately available.
- 0 if a value is not immediately available.

### 010 BSL

Reserved for future specification.

Current plan is Bit Shift Left.

Unsure if swizzle or append 0 is the most useful approach.

### 011 CMP

`CMP [DST][SRC]` compares the values in the `[SRC]` and `[DST]` registers.

The result is written to a temporary register whose result is:
- Usable in the next cycle.
- Then cleared.

This temporary register is shared with HAS

- +1 if `[DST]` is larger than `[SRC]`
-  0 if `[DST]` is equal to `[SRC]`
- -1 if `[DST]` is smaller than `[SRC]`

### 100 ADD

`ADD [DST][SRC]` adds the values in the `[SRC]` and `[DST]` registers.

The result is written to the `[DST]` register.

### 101 XOR

`XOR [DST][SRC]` performs a bitwise XOR on the values in the `[SRC]` and `[DST]` registers.

The result is written to the `[DST]` register.

### 110 JEZ

`JEZ [DST][SRC]` performs an absolute jump to the instruction at the address in the `[DST]` register if the value in the `[SRC]` register is zero.

This sets the `PC` register to the value in the `[DST]` register.

### 111 JGZ

`JGZ [DST][SRC]` performs an absolute jump to the instruction at the address in the `[DST]` register if the value in the `[SRC]` register is greater than zero.

This sets the `PC` register to the value in the `[DST]` register.

## Literals

The `IMM` register resolves to the value in the space immediately after the current instruction, as represented by `PC`.

This means that an instruction can have a value after itself, and read from this value as a literal by reading from the `IMM` register.

`PC` is incremented with every `IMM` access. Control flow continues to the next instruction not read as a literal, unless `PC` is modified by this instruction directly.

This means it is valid to have literals in program code which do not represent a meaningful instruction.

## Metaprogramming

Macros compose common reusable functionality from the basic instructions. Macros are strictly metaprogramming.

A macro is executed in the number of cycles it takes to execute the underlying instructions.

The following are some examples of how to compose instructions:

No-op. Does nothing, implemented as copying `ACC` to itself:

```
NOP =
    MOV [ACC] [ACC]
```

Negation. Inverts the sign of a value in `DST`, by using `XOR` with a literal of all set bits to invert all bits:

```
NEG[DST] = 
    XOR [DST] [IMM]
      1 11111 11111
```

Subtraction. Composing from the negation macro, storing the result of subtracting `SRC` from `DST` in `DST`:

```
SUB[DST][SRC] = 
    NEG[SRC]
    ADD[DST][SRC]
```

Robust subtraction. As above, but with the property that `SUB[DST][DST] = 0`:

```
RSUB[DST][SRC][TMP] =
    MOV [TMP][SRC]
    SUB [DST][TMP]
```

## Registers

The following registers are available for use by instructions as `[SRC]` and `[DST]`:

### 0000 NIL

Psuedo-register. Reads are always 0. Writes to `NIL` have no effect.

### 0001 ACC

The accumulator register. `ACC` is the first general purpose register. Values can be written to and read from `ACC` without side effects.

### 0010 BAK

The backup register. `BAK` is the second general purpose register. Values can be written to and read from `BAK` without side effects.

### 0011 IMM

Immediate code. `IMM` is used to access literal values in program code.

Reading from `IMM` increments the `PC` register with every access, so an instruction can read two literals.

Writing to `IMM` modifies program code.

### 0100 LEFT

The first inter-core bus. `LEFT` represents communication with the core to the left. If this core is the leftmost core on the grid, it wraps to the rightmost core on the grid in the same row.

Communication is half duplex, and for a single value.

Writing to `LEFT` makes that value available to the core to the left in its `RIGHT` register.

Writing to `LEFT` while the core to the left is writing to its `RIGHT` register is an error.

Writing to `LEFT` causes the current core to block, repeating transmission on every cycle without executing additional code until the core to the left reads the value from its `RIGHT` or `ANY` register.

Reading from `LEFT` causes the current core to block, repeating reception on every cycle without executing additional code until the core to the left writes the value to its `RIGHT`, `ANY`, or `ALL` register.

Reading from `LEFT` while the core to the left is reading from its `RIGHT` register is an error.

### 0101 RIGHT

The second inter-core bus. `RIGHT` represents communication with the core to the right. If this core is the rightmost core on the grid, it wraps to the leftmost core on the grid in the same row.

Communication is half duplex, and for a single value.

Writing to `RIGHT` makes that value available to the core to the right in its `LEFT` register.

Writing to `RIGHT` while the core to the right is writing to its `LEFT` register is an error.

Writing to `RIGHT` causes the current core to block, repeating transmission on every cycle without executing additional code until the core to the right reads the value from its `LEFT` or `ANY` register.

Reading from `RIGHT` causes the current core to block, repeating reception on every cycle without executing additional code until the core to the right writes the value to its `LEFT`, `ANY`, or `ALL` register.

Reading from `RIGHT` while the core to the right is reading from its `LEFT` register is an error.

### 0110 UP

The third inter-core bus. `UP` represents communication with the core above. If this core is the topmost core on the grid, it wraps to the bottommost core on the grid in the same column.

Communication is half duplex, and for a single value.

Writing to `UP` makes that value available to the core above in its `DOWN` register.

Writing to `UP` while the core above is writing to its `DOWN` register is an error.

Writing to `UP` causes the current core to block, repeating transmission on every cycle without executing additional code until the core above reads the value from its `DOWN` or `ANY` register.

Reading from `UP` causes the current core to block, repeating reception on every cycle without executing additional code until the core above writes the value to its `DOWN`, `ANY`, or `ALL` register.

Reading from `UP` while the core above is reading from its `DOWN` register is an error.

### 0111 DOWN

The fourth inter-core bus. `DOWN` represents communication with the core below. If this core is the bottommost core on the grid, it wraps to the topmost core on the grid in the same column.

Communication is half duplex, and for a single value.

Writing to `DOWN` makes that value available to the core below in its `UP` register.

Writing to `DOWN` while the core below is writing to its `UP` register is an error.

Writing to `DOWN` causes the current core to block, repeating transmission on every cycle without executing additional code until the core below reads the value from its `UP` or `ANY` register.

Reading from `DOWN` causes the current core to block, repeating reception on every cycle without executing additional code until the core below writes the value to its `UP`, `ANY`, or `ALL` register.

Reading from `DOWN` while the core below is reading from its `UP` register is an error.

### 1000 ANY

The first inter-core alias. `ANY` represents communication with any adjacent core.

If multiple adjacent cores attempt to read from their directional register corresponding to this core simultaneously, all cores receive the same value immediately.

Writing to `ANY` causes the current core to block, repeating transmission on every cycle without executing additional code until at least one adjacent core reads the value from its link to this core.

Reading from `ANY` causes the current core to block, repeating reception on every cycle without executing additional code until at least one adjacent core writes a value to on its link to this core.

### 1001 LAST

The second inter-core alias. `LAST`represents the register corresponding to the directional communication was received from or sent to the last time this core accessed an inter-core register.

### 1010 ALL

The sixth inter-core register. `ALL` represents communication with all adjacent cores.

Writing to `ALL` causes the current core to block, repeating transmission on every cycle without executing additional code until all adjacent cores have read the value from their directional register corresponding to this core.

An adjacent core cannot read from the same `ALL` transmission more than once. It will instead block until the next distinct instruction writing to `ALL` or its specific directional register.

Reading from `ALL` is an error.

This requires further thought as to implementation or requirements.

### 1011 IO

Reading from `IO` accesses the address defined by the `MA` register in io memory and returns the value stored there.

Writing from `IO` writes to the address defined by the `MA` register in io memory and returns the value stored there.

### 1100 PC

Program counter register. Specifies the address in `PM` of the next instruction to execute. Writing to this register has the same effect as an unconditional jump.

If this is written to, it blocks `PC` being updated that cycle.

A `PC` overflow is not an error, the program continues executing from `PC` = 0.

### 1101 PM

The program memory of the core.

`PC` specifies the address which is being executed.

Writing to this has the effect of changing the program being executed.

Reading from `PM` accesses the address defined by the `MA` register in program memory and returns the value stored there.

Writing from `PM` writes to the address defined by the `MA` register in program memory and returns the value stored there.

A program should return to `PC` = 0 at the end of the code block being executed.

This may mean a 2 byte instruction is required:
    MOV `PC` `IMM`
    0x00000 00000

### 1110 MA

The memory address register. `MA` is a special register used in reading and writing to a set of memory.

The `MA` register defines the address accessed when executing `IO`, `PM` and `MEM`.

### 1111 MEM

The shared memory between all cores.

Reading from `MEM` accesses the address defined by the `MA` register in general memory and returns the value stored there.

Writing from `MEM` writes to the address defined by the `MA` register in general memory and stores the specified value there.

## Value representation

Values are stored as ones' complement, 11-bit integers. The most significant bit is the sign bit. The remaining 10 bits are the magnitude of the value.

```
0 _____ _____ NEG FLAG
_ 00000 00000 2^10 BYTE

 0 11111 11111 = +1024
 0 00000 00000 = +0
 1 11111 11111 = -0
 1 00000 00000 = -1024
```

## Notes

- Cycles are synchronized between all cores.
- All computation happens simultaneously. Then, all `PC` registers are updated simultaneously.
- If the system's state is exactly the same as the previous one, without waiting for external I/O, an error indicating a deadlock is raised.
- If a core needs to look off the "edge" of the grid while linking to an adjacent core, it wraps around to the core on the other end of the same row/column.
- `PC` will automatically wrap to the start of the program, if it would auto-increment past the end of the program. Writing an out of bounds value to `PC` is an error. Writing to `IMM` cannot change the size of the program at runtime.
