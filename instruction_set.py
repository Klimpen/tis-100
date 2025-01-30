from constants import *

# need to think about how to do multiple immediates from a function call
# TODO rewrite these to use eachother where possible - or at least binary operators rather than inbuilt pythong stuff

class instruction_set:
    # 000
    def mov(core, dst, src):
        # places the value of src in dst
        # needs logic to handle fetching
        #   mem_fetch via mem_controller?
        #   adj_fetch via left/right/up/down - requires threadlock until successful
        #   immediate fetch

        # pc should not change if it's in access lock

        dst = src
        core.success = True


    # 001
    def has(core, src):
        # checks to see if the src has something to fetch
        # returns 0 if it does not
        # returns 1 if it does
        pass 

    # 010 - bit shift left
    def bsl(core, dst):
        # swizzle or append 0, unsure which
        pass

    # 011 - compare
    def cmp(core, dst, src):
        # returns   +1 if dst > src
        # returns   -1 if dst < src
        # returns +/-0 if dst = src
        pass

    # 100
    def add(core, dst, src):
        # sets dst = dst + src
        dst += src
        core.success = True

    # 101
    def xor(core, dst, src):
        # sets dst = dst xor src
        pass

    # 110
    def jez(core, dst, src):
        # jumps to dst
        # jumps if src == +0
        if src == 0:
            core.program_counter = dst
            core.success = False # dont increment the PC as we've set it manually

    # 111
    def jgz(core, dst, src):
        # jumps to dst
        # jumps if src > +0
        if src > 0:
            core.program_counter = dst
            core.success = False # dont increment the PC as we've set it manually
        else:
            core.success = True

    def decode(core, instruction):
        print("decoding")