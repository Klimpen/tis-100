from constants import *

class Instruction_Set:
    # 000
    def mov(core, dst, src):
        # places the value of src in dst
        # needs logic to handle fetching
        #   mem_fetch via mem_controller?
        #   adj_fetch via left/right/up/down - requires threadlock until successful
        #   immediate fetch

        # pc should not change if it's in access lock
        print(f"MOV: {dst}, {src}")

    # 001
    def has(core, dst, src):
        # read src.value
        print(f"HAS: {dst}, {src}")

    # 010 - bit shift left
    def bsl(core, dst, src):
        print(f"BSL: {dst}, {src}")

    # 011 - compare
    def cmp(core, dst, src):
        # read dst.value
        # read src.value

        # ans =   +1 if dst.value > src.value
        # ans =   -1 if dst.value < src.value
        # ans = +/-0 if dst.value = src.value

        # write ans to core.result

        print(f"CMP: {dst}, {src}")

    # 100
    def add(core, dst, src):
        # read dst.value
        # read src.value
        # ans = dst.value + src.value
        # write ans to dst
        print(f"ADD: {dst}, {src}")

    # 101
    def xor(core, dst, src):
        # read dst.value
        # read src.value
        # ans = dst.value ^ src.value
        # write ans to dst
        print(f"XOR: {dst}, {src}")

    # 110
    def jez(core, dst, src):
        # read src->src.value
        # if src.value == +/- 0
        # mov pc, dst
        print(f"JEZ: {dst}, {src}")

    # 111
    def jgz(core, dst, src):
        # read src->src.value
        # if src.value > +0
        # mov pc, dst
        print(f"JGZ: {dst}, {src}")