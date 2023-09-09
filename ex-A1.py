# Average simulation numbers of four algorithms (Experiment A1)
import math
import numpy as np
from util import okamoto, cp_int, interval_sensitive_bound


eps = 0.1
delta = 0.1
delta1 = 0.05 * delta

M = okamoto(eps, delta)
print(M)
n1 = interval_sensitive_bound(eps, delta, 0, 1)
print(n1)

p_list = np.arange(0.0, 1.01, 0.01)

p_xx = np.zeros_like(p_list)
p_yy = np.zeros_like(p_list)
p_oo = np.ones_like(p_list) * M  # the Okamoto bound
p_kk = np.ones_like(p_list) * n1  # our simple estimation algorithm
round_num = 100

# our adaptive estimation algorithm
for ii in range(len(p_list)):
    p = p_list[ii]
    count = 0
    for kk in range(round_num):
        n2 = max(min(math.ceil(0.01 * n1), 100), 10)
        count += n2
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
            count += n1
        else:
            n4 = n_list[N_num.index(m)]
            count += n4
            Np = np.random.binomial(n4, p, 1)[0]
            cp_l, cp_h = cp_int(n4, Np, delta1)
            count += interval_sensitive_bound(eps, (delta - delta1) / (1 - delta1), cp_l, cp_h)
    p_xx[ii] = count / round_num

print(p_xx)

# Massart bound-based algorithm
for ii in range(len(p_list)):
    p = p_list[ii]
    count = 0
    for kk in range(round_num):
        k = 0  # trial
        m = 0  # success
        nk = M
        cp_l = 0
        cp_h = 1
        while k < nk:
            k += 1
            m += np.random.binomial(1, p, 1)[0]
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
        count += k
    p_yy[ii] = count / round_num

print(p_yy)
