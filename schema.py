'''
Nomenclature:

- Schema: A definition of the dimensions of a grid of cores, and the programs to run on those cores.
- Grid: A 2D array of cores.
- Core: A single core in the grid.
- Byte: A single 11-bit value in the architecture.
- Program: Mixed instructions and data running or to be run on one core.
'''

from collections import frozendict
from constants import Byte, Instruction, Register
from itertools import takewhile
from grid import Grid
from typing import Iterable

Program = Iterable[Byte]

class Schema(object):
    '''
    A Schema defines the dimensions of a grid of cores, and the programs to be run on those cores.

    It is immutable, but can instantiate a Grid to execute the programs.
    '''
    __slots__ = ['_core_programs']

    def __init__(self, cores_w: int, cores_h: int, core_programs: Iterable[Program]):
        it = iter(core_programs)
        self._core_programs = tuple(
            tuple(
                tuple(next(it))
            ) for x in range(cores_w)
        for y in range(cores_h))

        # Sanity check: Makes sure we don't have excess
        if next(it, None) is not None:
            raise ValueError("Program specification has too many scripts")

    @classmethod
    def from_assembly(cls, cores_w: int, cores_h: int, scripts: Iterable[str]) -> 'Schema':
        '''
        Produce a Schema with the given dimensions and programs.
        '''
        def line_to_byte(line: str) -> Byte:
            match line.split():
                case [inst_str, dst_str, src_str]:
                    instruction = Instruction[inst_str]
                    dst = Register[dst_str]
                    src = Register[src_str]
                    return Byte.from_packed(instruction, dst, src)
                case [word]:
                    return Byte(int(word))
                case _:
                    raise ValueError("Invalid line: " + line)

        programs = ((line_to_byte(line) for line in script) for script in scripts)
        return Schema(cores_w, cores_h, programs)

    @classmethod
    def from_single_assembly(cls, script: str) -> 'Schema':
        '''
        Produce a Schema with a single program running on a single core.
        '''
        return cls.from_assembly(1, 1, (script,))

    def instantiate(self) -> Grid:
        '''
        Produce a Grid from this Schema.
        '''
        return Grid(len(self._core_programs[0]), len(self._core_programs), self._core_programs)
