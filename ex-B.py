# Case Study (Experiment B)
import math
import time
from zeroconf import zeroconf
from grid_world import grid_world
from util import okamoto, cp_int, interval_sensitive_bound, validate


def estimate(n, delta, a, b, eps, smc_model, para_list):
    # Algorithm 3 in paper
    if n == 0:
        return (a + b) / 2
    if not validate(n, delta, a, b, eps):
        est_count = 0
        n1 = okamoto(eps, delta)
        for i in range(n1):
            if smc_model(para_list):
                est_count += 1
        return est_count / n1
    else:
        est_count = 0
        for i in range(n):
            if smc_model(para_list):
                est_count += 1
        lb, ub = cp_int(n, est_count, delta)
        if ub <= a:
            return a
        elif lb >= b:
            return b
        else:
            return (max(lb, a) + min(ub, b)) / 2


eps = 0.1
delta = 0.1
delta1 = 0.05 * delta

M = okamoto(eps, delta)
print(M)
M2 = interval_sensitive_bound(eps, delta, 0, 1)
print(M2)

# Case Study 1: zeroconf parameter
# smc_model = zeroconf
# para_list = [(0.988564, 0.99, 1000), (0.990160, 0.99, 1000), (0.990852, 0.99, 1000),
#              (0.992489, 0.99, 1000), (0.993231, 0.99, 1000), (0.994036, 0.99, 1000), (0.994572, 0.99, 1000),
#              (0.995012, 0.99, 1000), (0.995415, 0.99, 1000)]
# print('zeroconf')

# Case Study 2: grid world parameter
smc_model = grid_world
para_list = [(0.5, 0.5, 0.4, ['time', 1000]), (0.5, 0.5, 0.5, ['time', 1000]), (0.5, 0.5, 0.6, ['time', 1000]),
             (3.0, 0.5, 0.4, ['meet']), (0.8, 0.5, 0.5, ['meet']), (0.5, 0.5, 0.6, ['meet'])]
print('grid world')

round_num = 100

for para_num in range(len(para_list)):
    print(para_list[para_num])
    # the Okamoto bound
    a = time.perf_counter()
    okamoto_result = []
    for i in range(round_num):
        M = okamoto(eps, delta)
        count = 0
        for j in range(M):
            if smc_model(para_list[para_num]):
                count += 1
        okamoto_result.append(count / M)
    print(okamoto_result)

    # our simple estimation algorithm (Algorithm 5 in paper)
    b = time.perf_counter()
    simple_result = []
    for i in range(round_num):
        M2 = interval_sensitive_bound(eps, delta, 0, 1)
        simple_result.append(estimate(M2, delta, 0, 1, eps, smc_model, para_list[para_num]))
    print(simple_result)

    # our adaptive estimation algorithm (Algorithm 6 in paper)
    c = time.perf_counter()
    adaptive_result = []
    simulation_num = 0
    for kk in range(round_num):
        n1 = interval_sensitive_bound(eps, delta, 0, 1)
        n2 = max(min(math.ceil(0.01 * n1), 100), 10)
        simulation_num += n2
        count_1 = 0
        for j in range(n2):
            if smc_model(para_list[para_num]):
                count_1 += 1
        p_1 = count_1 / n2

        n_list = [round((i + 1) * n1 / 100) for i in range(20)]
        length = len(n_list)
        cost = n_list.copy()
        for i in range(length):
            n3 = n_list[i]
            Np = round(n3 * p_1)
            cp_l, cp_h = cp_int(n3, Np, delta1)
            cost[i] += interval_sensitive_bound(eps, (delta - delta1) / (1 - delta1), cp_l, cp_h)
        m = min(cost)
        if m > n1:
            adaptive_result.append(estimate(n1, delta, 0, 1, eps, smc_model, para_list[para_num]))
            simulation_num += n1
        else:
            n4 = n_list[cost.index(m)]
            simulation_num += n4
            count_2 = 0
            for j in range(n4):
                if smc_model(para_list[para_num]):
                    count_2 += 1
            cp_l, cp_h = cp_int(n4, count_2, delta1)
            n5 = interval_sensitive_bound(eps, (delta - delta1) / (1 - delta1), cp_l, cp_h)
            simulation_num += n5
            adaptive_result.append(
                estimate(n5, (delta - delta1) / (1 - delta1), cp_l, cp_h, eps, smc_model, para_list[para_num]))
    print(simulation_num / round_num)
    print(adaptive_result)

    # Massart bound-based algorithm
    d = time.perf_counter()
    massart_result = []
    simulation_num_massart = 0
    for kk in range(round_num):
        M = okamoto(eps, delta)
        k = 0  # trial
        m = 0  # success
        nk = M
        cp_l = 0
        cp_h = 1
        while k < nk:
            k += 1
            if smc_model(para_list[para_num]):
                m += 1
            cp_l, cp_h = cp_int(k, m, delta1)
            if cp_l <= 0.5 <= cp_h:
                nk = M
            elif cp_h < 0.5:
                nk = math.ceil(
                    math.log(2 / (delta - delta1)) * 2 * (3 * cp_h + eps) * (3 - 3 * cp_h - eps) / (9 * eps * eps))
            else:
                nk = math.ceil(
                    math.log(2 / (delta - delta1)) * 2 * (3 - 3 * cp_l + eps) * (3 * cp_l - eps) / (9 * eps * eps))
            nk = min(nk, M)
        simulation_num_massart += k
        massart_result.append(m / k)
    print(simulation_num_massart / round_num)
    print(massart_result)
    e = time.perf_counter()

    print('okamoto time:', b - a)
    print('simple time:', c - b)
    print('adaptive time:', d - c)
    print('massart time:', e - d)
