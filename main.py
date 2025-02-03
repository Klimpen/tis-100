from core import *
from constants import *
from instruction_set import *


def main():

    cores = []

    #init cores - up/down wrapping and right/left wrapping - torus of cores!
    for i in range(0, CORES_WIDTH):
        sub_list = []
        for j in range(0, CORES_HEIGHT):
            sub_list.append(Core())

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
        # executes current instruction
        for sub_list in cores:
            for core in sub_list:
                core.run()
        
        # updates pc
        for sub_list in cores:
            for core in sub_list:
                core.update_program_counter()


if __name__ == "__main__":
    main()

