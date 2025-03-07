import os
from time import sleep

from core import *
from constants import *
from draw import *
from programs import Schemas

from typing import Tuple

def main():
    draw = Draw()
    grid = Schemas.mutating_test_one.instantiate()

    while(True):
        render(draw, grid)
        grid.process()
        sleep(0.5)

def clear_screen():
    print('\x1b[2J')

def render(draw, cores):
    clear_screen()
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

