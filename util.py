import math
from scipy.special import betaincinv


def okamoto(eps, delta):
    # the Okamoto bound
    return math.ceil(math.log(2 / delta) / (2 * eps * eps))


def cp_int(N, Np, delta, side='both'):
    # Clopper_pearson confidence interval
    assert (side == 'both' or side == 'right' or side == 'left')
    if side != 'right':
        if Np == 0:
            cp_l = 0
        else:
            cp_l = betaincinv(Np, N - Np + 1, delta / 2)
        if side == 'left':
            return cp_l
    if Np == N:
        cp_h = 1
    else:
        cp_h = betaincinv(Np + 1, N - Np, 1 - delta / 2)
    if side == 'right':
        return cp_h
    return cp_l, cp_h


def intersect(a, b, c, d):
    # return the length of intersection of [a,b] and [c,d]
    return max(min(b, d) - max(a, c), 0)


def margin_left(n, delta, a):
    # find k, such that CP(n,k).left<=a,CP(n,k+1).left>a
    assert cp_int(n, n, delta, 'left') > a
    low = 0
    high = n
    while high - low > 1:
        mid = (high + low) // 2
        if cp_int(n, mid, delta, 'left') > a:
            high = mid
        else:
            low = mid
    return low


def margin_right(n, delta, b):
    # find k, such that CP(n,k).right<b,CP(n,k+1).right>=b
    assert cp_int(n, 0, delta, 'right') < b
    low = 0
    high = n
    while high - low > 1:
        mid = (high + low) // 2
        if cp_int(n, mid, delta, 'right') >= b:
            high = mid
        else:
            low = mid
    return low


def max_length(n, delta, a, b):
    # Algorithm 2 in paper
    # return the max length of CP(n,k,delta)∩[a,b], k=0,1,...,n
    if cp_int(n, 0, delta, 'right') >= b or cp_int(n, n, delta, 'left') <= a:
        return b - a
    k1 = margin_left(n, delta, a)
    k2 = margin_right(n, delta, b)
    l1, h1 = cp_int(n, k1, delta)
    l2, h2 = cp_int(n, k1 + 1, delta)
    l3, h3 = cp_int(n, k2, delta)
    l4, h4 = cp_int(n, k2 + 1, delta)
    l5, h5 = cp_int(n, n // 2, delta)
    return max(intersect(a, b, l1, h1), intersect(a, b, l2, h2), intersect(a, b, l3, h3), intersect(a, b, l4, h4),
               intersect(a, b, l5, h5))


def interval_sensitive_bound(eps, delta, a, b):
    # Algorithm 1 in paper
    if b - a <= 2 * eps:
        return 0
    low = 0
    high = okamoto(eps, delta)
    while high - low > 1:
        mid = (high + low) // 2
        if max_length(mid, delta, a, b) <= 2 * eps:
            high = mid
        else:
            low = mid
    return high


def validate(n, delta, a, b, eps):
    # Algorithm 4 in paper
    # validate if the max length of CP(n,k)∩[a,b] <= 2*eps (k=0,1,...,n)
    if cp_int(n, 0, delta, 'right') >= b or cp_int(n, n, delta, 'left') <= a:
        if b - a <= 2 * eps:
            return True
        else:
            print('WARNING! Validate failure 1', n, delta, a, b, eps)
            return False
    k1 = margin_left(n, delta, a)
    k2 = margin_right(n, delta, b)
    for i in range(k1, k2 + 1, 1):
        l, h = cp_int(n, i, delta)
        if intersect(a, b, l, h) > 2 * eps:
            print('WARNING! Validate failure 2', n, delta, a, b, eps)
            return False
    return True

