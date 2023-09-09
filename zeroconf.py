# IPv4 zeroconf Protocol，see "Principles of Model Checking" p751 Example10.5
import random


def zeroconf(para_list):
    # r: information lost probability
    # q: IP address occupancy rate
    # n: number of confirmations
    r, q, n = para_list[0], para_list[1], para_list[2]
    state = 0
    while True:
        x = random.random()
        if state == 0:
            if x < q:
                state = 1
            else:
                return False  # success(state=n+1)
        elif state == n:
            if x < r:
                return True  # fail(state=n+2)
            else:
                state = 0
        else:
            if x < r:
                state += 1
            else:
                state = 0

