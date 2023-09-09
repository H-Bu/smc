# delta' sensitivity (Experiment A3)
import math
import numpy as np
from util import cp_int, interval_sensitive_bound


eps = 0.1
delta = 0.1
k = [0.01, 0.02, 0.05, 0.10, 0.20]  # delta'=k*delta
print('eps:', eps, 'delta:', delta)

n1 = interval_sensitive_bound(eps, delta, 0, 1)

for x in range(5):
    print(k[x])
    delta1 = k[x] * delta
    p_list = np.arange(0.0, 1.01, 0.01)
    p_xx = np.zeros_like(p_list)
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
    print(sum(p_xx) / len(p_xx))
