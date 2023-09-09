# soundness check (Experiment A2)
import math
import numpy as np
from util import okamoto, cp_int, interval_sensitive_bound, validate


def estimate(n, delta, a, b, eps):
    if n == 0:
        return (a + b) / 2
    if not validate(n, delta, a, b, eps):
        n1 = okamoto(eps, delta)
        est_oka = np.random.binomial(n1, p, 1)[0] / n1
        return est_oka
    else:
        success = np.random.binomial(n, p, 1)[0]
        lb, ub = cp_int(n, success, delta)
        if ub < a:
            return a
        elif lb > b:
            return b
        else:
            return (max(lb, a) + min(ub, b)) / 2


eps = 0.01
delta = 0.01
delta1 = 0.05 * delta

M = okamoto(eps, delta)
print(M)
n1 = interval_sensitive_bound(eps, delta, 0, 1)
print(n1)

p_list = np.arange(0., 1.01, 0.01)

p_xx = np.zeros_like(p_list)
p_yy = np.zeros_like(p_list)

round_num = 100000

# our adaptive estimation algorithm
for ii in range(len(p_list)):
    p = p_list[ii]
    count_fail = 0
    for kk in range(round_num):
        n2 = max(min(math.ceil(0.01 * n1), 100), 10)
        count_1 = np.random.binomial(n2, p, 1)[0]
        p_1 = count_1 / n2

        n_list = [round((i + 1) * n1 / 100) for i in range(20)]
        length = len(n_list)
        N_num = n_list.copy()
        for i in range(length):
            n3 = n_list[i]
            Np = round(n3 * p_1)
            cp_l, cp_h = cp_int(n3, Np, delta1)
            N_num[i] += interval_sensitive_bound(eps, (delta - delta1) / (1 - delta1), cp_l, cp_h)
        m = min(N_num)
        if m > n1:
            est = estimate(n1, delta, 0, 1, eps)
            if est < p - eps or est > p + eps:
                count_fail += 1
        else:
            n4 = n_list[N_num.index(m)]
            Np = np.random.binomial(n4, p, 1)[0]
            cp_l, cp_h = cp_int(n4, Np, delta1)
            num = interval_sensitive_bound(eps, (delta - delta1) / (1 - delta1), cp_l, cp_h)
            est = estimate(num, (delta - delta1) / (1 - delta1), cp_l, cp_h, eps)
            if est < p - eps or est > p + eps:
                count_fail += 1
    p_xx[ii] = count_fail / round_num

print(p_xx)

# our simple estimation algorithm
l = [0.] * (n1 + 1)
h = [0.] * (n1 + 1)
for i in range(n1 + 1):
    l[i], h[i] = cp_int(n1, i, delta)
for ii in range(len(p_list)):
    p = p_list[ii]
    count_fail = 0
    tmp = np.random.binomial(n1, p, round_num)
    for kk in range(round_num):
        result = tmp[kk]
        if abs((l[result] + h[result]) / 2 - p) > eps:
            count_fail += 1
    p_yy[ii] = count_fail / round_num

print(p_yy)
