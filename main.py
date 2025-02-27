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

    program = Programs.mutating_test_one()
    program_core = Parse_Program(program[2:]).programs
    draw = Draw()
    
    for i in range(0, program[0]):
        sub_list = []
        for j in range(0, program[1]):
            sub_list.append(Core(program_core[i*program[1]+j], memory, io))
            if program[1] > 1:
                if not j == 0:
                    sub_list[-1].left = sub_list[-2].right
                if j+1 == program[1]:
                    sub_list[0].left = sub_list[-1].right
            if program[0] > 1:
                if not i == 0:
                    cores[i-1][j].down = sub_list[-1].up
                if i+1 == program[0]:
                    sub_list[-1].down = cores[0][j].up

        cores.append(sub_list)

    while(True):
        render(draw, cores)
        run(cores)
        update(cores)
        sleep(0.25)

def render(draw, cores):
    os.system('clear')
    for sub_list in cores:
        lines = [""] * 18
        for core in sub_list:
            core_draw = draw.draw(core)
            for i in range(0, len(core_draw)):
                lines[i]+=core_draw[i]
        for line in lines:
            print(line)

def run(cores):
    for sub_list in cores:
        for core in sub_list:
            core.run()

def update(cores):
    for sub_list in cores:
        for core in sub_list:
            core.update()

if __name__ == "__main__":
    main()

