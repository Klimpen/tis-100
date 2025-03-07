from typing import Optional

from constants import *
from instruction_set import *

class Core():

    def __init__(self, memory_program: list[Byte], memory_general: list[Byte], memory_io: list[Byte], read_io: Byte):
        
        self.memory_general = memory_general
        self.memory_address: int = 0

        self.memory_io: list[Byte] = memory_io
        self.read_io: Byte = read_io

        self.memory_program: list[Byte] = memory_program
    
        self.program_counter: int = 0

        self.acc = Byte(0b0)
        self.bak = Byte(0b0)

        self.result = None      # TODO: Figure this - placeholder
        # XXX: Pending Grid processing phase rework
        self.blocked = False    # DEFAULT = False, reset to False each tick. True = do not increment program_counter; False = increment program_counter


        self.left = None        # contains a bus
        self.right = Bus()      # these bus are shared registers between adjacent cores
        self.up = Bus()
        self.down = None

    def has_value(self, address: Register) -> bool:
        match address:
            case Register.LEFT:
                return self.left.send
            case Register.RIGHT:
                return self.right.send
            case Register.UP:
                return self.up.send
            case Register.DOWN:
                return self.down.send

            case Register.ANY:
                return self.has_any()
            case Register.LAST:
                return self.has_last()
            case Register.ALL:
                return self.has_all()
            case _: Exception(address)

    def has_any(self) -> bool:
        return any((
            self.left.send,
            self.right.send,
            self.up.send,
            self.down.send
        ))

    def has_last(self) -> bool:
        pass

    def has_all(self) -> bool:
        return all((
            self.left.send,
            self.right.send,
            self.up.send,
            self.down.send
        ))

    def get_value(self, address: Register) -> Byte:
        
        match address:
            case Register.NIL:
                return 0b0
            case Register.ACC:
                return self.acc.value
            case Register.BAK:
                return self.bak.value
            case Register.IMM:
                return self.get_immediate()

            case Register.LEFT:
                return self.get_direction(self.left)
            case Register.RIGHT:
                return self.get_direction(self.right)
            case Register.UP:
                return self.get_direction(self.up)
            case Register.DOWN:
                return self.get_direction(self.down)

            case Register.ANY:
                return self.get_any()
            case Register.LAST:
                return self.get_last()
            case Register.ALL:
                raise Exception("Cannot read from ALL") # cannot read from ALL
            case Register.IO:
                return self.read_io

            case Register.PC:
                return self.program_counter
            case Register.PM:
                return self.get_memory(self.memory_program)
            case Register.MA:
                return self.memory_address
            case Register.MEM:
                return self.get_memory(self.memory_general)
            case _:
                raise Exception('Unknown Register to read from: ' + address)

    def get_immediate(self) -> Byte:
            self.program_counter += 1
            self.program_counter %= len(self.memory_program)

            return self.memory_program[self.program_counter].value

    def get_direction(self, direction: Bus) -> Optional[Byte]:
        value = direction.read()

        if value is None:
            self.blocked = True

        return value

    def get_any(self) -> Optional[Byte]:
        # case: there is something to get
        output = None

        if self.has_any():
            # XXX: Do we need to take every value from all directions?
            if self.left.send:
                output = self.get_direction(self.left)
            if self.right.send:
                output = self.get_direction(self.right)
            if self.up.send:
                output = self.get_direction(self.up)
            if self.down.send:
                output = self.get_direction(self.down)
            return output
        
        # case: there is not something to get
        self.blocked = False
        return output

    def get_last(self) -> Optional[Byte]:
        pass

    def get_memory(self, memory) -> Byte:
        return memory[self.memory_address].value
    
    def write_value(self, address: Register, value: Byte) -> None:

        checked_value = self.bounds_check(value)

        match address:
            case Register.NIL:
                pass
            case Register.ACC:
                self.acc.value = checked_value
            case Register.BAK:
                self.bak.value = checked_value
            case Register.IMM:
                self.write_immediate(checked_value)

            case Register.LEFT:
                self.write_direction(self.left, checked_value)
            case Register.RIGHT:
                self.write_direction(self.right, checked_value)
            case Register.UP:
                self.write_direction(self.up, checked_value)
            case Register.DOWN:
                self.write_direction(self.down, checked_value)

            case Register.ANY:
                self.write_any(checked_value)
            case Register.LAST:
                self.write_last(checked_value)
            case Register.ALL:
                self.write_all(checked_value)
            case Register.IO:
                self.write_memory(value, self.memory_io)

            case Register.PC:
                self.write_pc(checked_value)
            case Register.PM:
                self.write_memory(value, self.memory_program)
            case Register.MA:
                self.memory_address = checked_value
            case Register.MEM:
                self.write_memory(value, self.memory_general)
            case _:
                raise Exception('Unknown Register to write to: ' + address)
    
    def bounds_check(self, value: int) -> int:
        if value > 1024:
            value -= 2048
        if value < -1024:
            value += 2048
        return value
    
    def write_immediate(self, value: int) -> None:
        # XXX: This needs to advance PC too?
        self.memory_program[self.program_counter+1].value = value

    def write_direction(self, direction, value):
        self.blocked = direction.write(value)

    def write_any(self, value):
        pass

    def write_last(self, value):
        pass

    def write_all(self, value):
        pass

    def write_pc(self, value: int):
        self.program_counter = value
        self.blocked = True

    def write_memory(self, value, memory):
        memory[self.memory_address].value = value

    def run(self):        
        instruction = self.memory_program[self.program_counter].value
        self.execute(instruction)

    #TODO: update this to use 'add(pc, 0b1)'
    def update(self):
        if self.blocked:
            self.blocked = False
        else:
            self.program_counter += 1
            self.program_counter %= len(self.memory_program)


#   Each instruction is 1 byte
#   [3bit][4bit][4bit]
#   instruction - dst address - src address
    def execute(self, value: Byte):
        instruction, dst, src = value.unpack()
        
        match(instruction):
            case Instruction.MOV:
                InstructionSet.mov(self, dst, src)
            case Instruction.HAS:
                InstructionSet.has(self, dst, src)
            case Instruction.BSL:
                InstructionSet.bsl(self, dst, src)
            case Instruction.CMP:
                InstructionSet.cmp(self, dst, src)
            case Instruction.ADD:
                InstructionSet.add(self, dst, src)
            case Instruction.XOR:
                InstructionSet.xor(self, dst, src)
            case Instruction.JEZ:
                InstructionSet.jez(self, dst, src)
            case Instruction.JGZ:
                InstructionSet.jgz(self, dst, src)
            case _:
                raise Exception(instruction)
