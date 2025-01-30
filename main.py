from constants import *
from core import *


def main():

    cores = []

    #init cores - up/down wrapping and right/left wrapping - torus of cores!
    for i in range(0, CORES_WIDTH):
        sub_list = []
        for j in range(0, CORES_HEIGHT):
            new_core = Core()
            sub_list.append(new_core)

            if not j == 0:
                sub_list[-2].right = sub_list[-1]
                sub_list[-1].left = sub_list[-2]

            if j+1 == CORES_HEIGHT:
                sub_list[-1].right = sub_list[0]
                sub_list[0].left = sub_list[-1]

            if not i == 0:
                cores[i-1][j].down = sub_list[-1]
                sub_list[-1].up = cores[i-1][j]

            if i+1 == CORES_WIDTH:
                sub_list[-1].down = cores[0][j]
                cores[0][j].up = sub_list[-1]

        cores.append(sub_list)

    while(True):
        # executes current instruction
        for sub_list in cores:
            for core in sub_list:
                core.run()
        
        # updates pc
        for sub_list in cores:
            for core in sub_list:
                core.update()


if __name__ == "__main__":
    main()

