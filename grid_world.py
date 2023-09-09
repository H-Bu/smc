# Grid World，modified from Section 3.3 of "Numerical vs. statistical probabilistic model checking"
from numpy.random import exponential
import random


def next_1(x, y, r):
    # Given the current position (x,y) of robot, return the next position
    # r: return probability
    if random.random() < r:  # return to the bottom left grid
        return 1, 1
    elif x < 5:
        return x + 1, y
    else:
        return x, y + 1


def next_2(x, y):
    # Given the current position (x,y) of janitor, return the next position
    if 1 < x < 5 and 1 < y < 5:
        direct = random.randint(1, 4)
        if direct == 1:
            return x + 1, y
        elif direct == 2:
            return x, y + 1
        elif direct == 3:
            return x - 1, y
        else:
            return x, y - 1
    elif x == 1 and 1 < y < 5:
        direct = random.randint(1, 3)
        if direct == 1:
            return x + 1, y
        elif direct == 2:
            return x, y + 1
        else:
            return x, y - 1
    elif x == 5 and 1 < y < 5:
        direct = random.randint(1, 3)
        if direct == 1:
            return x, y + 1
        elif direct == 2:
            return x - 1, y
        else:
            return x, y - 1
    elif 1 < x < 5 and y == 1:
        direct = random.randint(1, 3)
        if direct == 1:
            return x + 1, y
        elif direct == 2:
            return x, y + 1
        else:
            return x - 1, y
    elif 1 < x < 5 and y == 5:
        direct = random.randint(1, 3)
        if direct == 1:
            return x + 1, y
        elif direct == 2:
            return x - 1, y
        else:
            return x, y - 1
    else:
        direct = random.randint(1, 2)
        if x == 1 and y == 1:
            if direct == 1:
                return 2, 1
            else:
                return 1, 2
        elif x == 1 and y == 5:
            if direct == 1:
                return 2, 5
            else:
                return 1, 4
        elif x == 5 and y == 1:
            if direct == 1:
                return 5, 2
            else:
                return 4, 1
        else:
            if direct == 1:
                return 4, 5
            else:
                return 5, 4


def grid_world(para_list):
    # lam_1, lam_2: moving rate of robot and janitor
    # return_p: return probability
    lam_1, lam_2, return_p, spec = para_list[0], para_list[1], para_list[2], para_list[3]
    total_time = 0  # current time
    meet = False  # meet janitor
    x_1, y_1 = 1, 1  # position of robot
    x_2, y_2 = 3, 3  # position of janitor
    t1 = exponential(1 / lam_1)
    t2 = exponential(1 / lam_2)
    while x_1 != 5 or y_1 != 5:
        if t1 < t2:  # robot takes a step
            total_time += t1
            t2 -= t1
            t1 = exponential(1 / lam_1)
            x, y = next_1(x_1, y_1, return_p)
            if x == x_2 and y == y_2:  # janitor is in the destination (MEET)
                meet = True
            else:
                x_1, y_1 = x, y
        else:  # janitor takes a step
            total_time += t2
            t1 -= t2
            t2 = exponential(1 / lam_2)
            x_2, y_2 = next_2(x_2, y_2)
    if spec[0] == 'time':
        return total_time < spec[1]
    else:
        assert spec[0] == 'meet'
    return meet

