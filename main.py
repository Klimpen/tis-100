from core import *
from constants import *
from parse_program import *
from programs import *
from draw import *
import os
from time import sleep

def main():

    cores = []
    memory = [Byte(0)] * 2**11
    io = [Byte(0)] * 2**11

    program = Programs.add_and_fib()
    program_core = Parse_Program(program[2:]).programs
    draw = Draw()
    
    #init cores - up/down wrapping and right/left wrapping - torus of cores!
    for i in range(0, program[0]):
        sub_list = []
        for j in range(0, program[1]):
            sub_list.append(Core(program_core[i*program[1]+j], memory, io))

            if not j == 0:
                sub_list[-1].left = sub_list[-2].right
            if j+1 == CORES_HEIGHT:
                sub_list[0].left = sub_list[-1].right

            if not i == 0:
                cores[i-1][j].down = sub_list[-1].up
            if i+1 == CORES_WIDTH:
                sub_list[-1].down = cores[0][j].up

        cores.append(sub_list)

    while(True):
        #draws state
        os.system('clear')
        for sub_list in cores:
            lines = [""] * 18
            for core in sub_list:
                core_draw = draw.draw(core)
                for i in range(0, len(core_draw)):
                    lines[i]+=core_draw[i]
            for line in lines:
                print(line)

        # executes current instruction
        for sub_list in cores:
            for core in sub_list:
                core.run()
        
        # updates pc
        for sub_list in cores:
            for core in sub_list:
                core.update_program_counter()
        
        sleep(0.25)


if __name__ == "__main__":
    main()

