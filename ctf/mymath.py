def dp(ary, limit, _index=0, _values=None, _stats=None):
    """
    Dynamic Programming as Knapsack problem
    :param ary: e.g. [[cost, value], [cost, value], [cost, value]...]
    :param limit: cost limit
    :param _index:
    :param _values: memorized table
    :param _stats: select item flag
    :return:
    """
    if _values is None:  # init memo table
        _stats = [False] * len(ary)
        _values = [[-1 for _ in range(len(ary))] for _ in range(limit + 1)]
    if _index == len(ary):  # last node
        return 0, _stats
    if _values[limit][_index] > -1:  # already discovered
        return _values[limit][_index], _stats
    if limit < ary[_index][0]:  # limit overflow
        return dp(ary, limit, _index + 1, _values, _stats)
    a = dp(ary, limit - ary[_index][0], _index + 1, _values, _stats)[0] + ary[_index][1]
    b = dp(ary, limit, _index + 1, _values, _stats)[0]
    if a > b and not _stats[_index]:
        _stats[_index] = True
    _values[limit][_index] = max(a, b)
    return _values[limit][_index], _stats


def pf_decomposition(n):
    """
    practicality factor is 14 digit or less
    10**12 : 0.7sec
    10**13 : 1.3sec
    10**14 : 6.4sec
    """
    i = 2
    factor = []
    while i ** 2 < n:
        e = 0
        while n % i == 0:
            n //= i
            e += 1
        if e > 0:
            factor.append([i, e])
        i += 1
    if n > 0:
        factor.append([n, 1])
    return factor


def binary_search(start_index, end_index, y, func=lambda x: x ** 101):
    mid = (end_index - start_index) // 2 + start_index
    while func(mid) != y:
        if func(mid) > y:
            end_index = mid
        elif func(mid) < y:
            start_index = mid
        mid = (end_index - start_index) // 2 + start_index
    return mid


def ext_gcd(a, b):
    if b > 0:
        y, x, d = ext_gcd(b, a % b)
        return x, y - a // b * x, d
    else:
        return 1, 0, a


def gcd(a, b):
    """ greatest common divisor
    """
    if b != 0:
        return gcd(b, a % b)
    else:
        return a


def lcm(a, b):
    """ least common multiple
    """
    
    return a // gcd(a, b) * b


def is_prime(n):
    i = 2
    while i * i < n:
        if n % i == 0:
            return False
        i += 1
    return True
