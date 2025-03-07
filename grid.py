
from constants import Bus, Byte

from core import Core
from itertools import chain
from schema import Program
from typing import Collection, Iterable, TypeVar

class Grid(object):
    __slots__ = ['_cores', '_grid', '_shared_memory', '_io', '_read_io']

    def __init__(self, cores_w, cores_h, core_programs: Collection[Collection[Program]]):
        # FIXME: Shared memory is modified in-place, rather than being deferred or double-buffered.
        # Currently, a core writing to shared memory can have the new value read by another core, if the other core is
        # processed later.
        self._shared_memory = [Byte(0) for _ in range (2**11)]

        # TODO: Not currently used in practice?
        self._read_io = Byte(0)

        # Instantiate a core for every program in the schema
        self._grid: tuple[tuple[Core]] = tuple(
            tuple(
                Core(list(program), self._shared_memory, self._io, self._read_io, )
                for x, program in enumerate(row)
            )
            for y, row in enumerate(core_programs)
        )
        # Ensure all Bus connections are linked correctly
        for y, row in enumerate(self._grid):
            for x, core in enumerate(row):
                core.left = self._grid[y][x-1].right
                core.down = self._grid[(y+1) % cores_h][x].up

        # Finally, store all cores and buses in a linearized form
        self._cores: tuple[Core] = tuple(*self._grid)
        self._buses: tuple[Bus] = tuple(chain.from_iterable((c.up, c.right) for c in self._cores))

    def process(self) -> None:
        # For coheernt simultaneous I/O, we'll need a three pass process.
        # The first pass will process one instruction from every core.
        # Cores which are blocked waiting for I/O will be marked as such, with buses flagged to indicate their state.
        # In the second pass, bus states will be resolved.
        # In the third pass, cores advance, if unblocked.

        # For now, the previous behaviour (run all cores, a core which supplies a value will have that value consumed
        # if the supplier core was processed before the consumer core) is preserved.
        self._run_all_cores()
        self._resolve_all_buses()
        self._advance_unblocked_cores()

    def _run_all_cores(self) -> None:
        '''
        Process one instruction from every core, where possible.

        This cause some core to block for I/O, to be handled by buses once they know the state of all of their
        neighbours.
        '''
        for c in self._cores:
            c.run()

    def _resolve_all_buses(self) -> None:
        '''
        Perform deferred I/O processing.
        '''
        pass

    def _advance_unblocked_cores(self) -> None:
        for c in self._cores:
            c.update()
