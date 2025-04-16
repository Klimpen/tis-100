from constants import *

class InstructionSet:
    # 000
    def mov(core, dst, src):
        # places the value of src in dst
        # needs logic to handle fetching
        #   mem_fetch via mem_controller?
        #   adj_fetch via left/right/up/down - requires threadlock until successful
        #   immediate fetch

        # pc should not change if it's in access lock
        
        # print(f"MOV: {dst}, {src}")

        src_value = core.get_value(src)
        
        core.write_value(dst, src_value)

    # 001
    def has(core, dst, src):
        # read src.value
        # if read is successful, core.result = 1
        # print(f"HAS: {dst}, {src}")
        src_value = core.has_value(src)

        if src_value:
            core.result = 1 

    # 010 - bit shift left
    # TODO figure how I want to do this
    def bsl(core, dst, src):
        # read src.value
        # src_value << 1 : bitshift left, append 0
        # write ans to dst
        # print(f"BSL: {dst}, {src}")
        src_value = core.get_value(src)

        src_value << 1

        core.write_value(dst, src_value)

    # 011 - compare
    def cmp(core, dst, src):
        # read dst.value
        # read src.value

        # core.result =   +1 if dst.value > src.value
        # core.result =   -1 if dst.value < src.value
        # core.result = +/-0 if dst.value = src.value


        # print(f"CMP: {dst}, {src}")

        dst_value = core.get_value(dst)
        src_value = core.get_value(src)

        if(dst_value > src_value):
            core.result = 1
        if(dst_value == src_value):
            core.result = 0
        if(dst_value < src_value):
            core.result = -1

    # 100
    def add(core, dst, src):
        # read dst.value
        # read src.value
        # ans = dst.value + src.value
        # write ans to dst
        # print(f"ADD: {dst}, {src}")

        dst_value = core.get_value(dst)
        src_value = core.get_value(src)

        ans = dst_value + src_value

        core.write_value(dst, ans)

    # 101
    def xor(core, dst, src):
        # read dst.value
        # read src.value
        # ans = dst.value xor src.value
        # write ans to dst
        # print(f"XOR: {dst}, {src}")

        dst_value = core.get_value(dst)
        src_value = core.get_value(src)

        ans = dst_value ^ src_value

        core.write_value(dst, ans)



    # 110
    def jez(core, dst, src):
        # read src->src.value
        # if src.value == +/- 0
        # mov pc, dst
        # print(f"JEZ: {dst}, {src}")

        src_value = core.get_value(src)

        if(src_value == 0):
            InstructionSet.mov(core, Instruction.PC, dst)

    # 111
    def jgz(core, dst, src):
        # read src->src.value
        # if src.value > +0
        # mov pc, dst
        # print(f"JGZ: {dst}, {src}")

        src_value = core.get_value(src)

        if(src_value > 0):
            InstructionSet.mov(core, Instruction.PC, dst)
