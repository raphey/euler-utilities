__author__ = 'raphey'
# python 2


from math import log
from my_utility_module import prod


# Based on code from http://code.activestate.com/recipes/366178-a-fast-prime-number-list-generator/
# Added my own comments to explain what's going on.
def primes(n):

    if n < 2:
        return []

    prime_list = [2]                        # deals with 2 on its own
    s = list(range(3, n + 1, 2))            # list of odd numbers from 3 to n
    mroot = n ** 0.5                        # Reminder: this is a float
    # half = int((n + 1) / 2 - 1)           # This is just the length of s. Removed from original code to simplify
    i = 0                                   # Starting with i indexed to the first odd number in list s
    m = 3                                   # m will be all the prime numbers <= sqrt(N), starting with 3
    while m <= mroot:
        if s[i]:
            j = int((m * m - 3) / 2)        # This sets j such that s[j] is m^2. Funny indexing math.
            s[j] = 0                        # This sets the initial m^2 as not prime (this is the first value that
                                            # need be considered, since m times anything smaller than m will already
                                            # have been sieved out
            while j < len(s):               # Loop stops when we try to label a non-prime outside the range N
                s[j] = 0                    # Set a value to non-prime (seems to be redundant on first pass)
                j += m                      # Jump ahead by m in the odd number list, meaning 2m in actual numbers
                                            # For example, for m = 3, after marking 9 non-prime, marks 15, 21, 27...
                                            # Some numbers still do get visited twice.
        i += 1                              # Move to next odd number index
        m = 2 * i + 3                       # Set m to the actual odd number in question
    prime_list.extend([x for x in s if x])
    return prime_list


def is_prime(n):
    if n == 1:
        return False
    n_root = int(n ** 0.5)
    for x in range(2, n_root + 1):
        if n % x == 0:
            return False
    return True


def fast_is_prime(n, jumpahead=10):
    """Checks if n is prime using a global variable storing primes. If it doesn't have enough primes to finish the
    check, it makes a new list of primes, up to a new limit of jumpahead times the minimum value used to evaluate the
    current n. (Otherwise, if you asked for consecutive primes, you'd be constantly rebuilding the list.)
    """
    if n == 1:
        return False

    global p_list

    n_root = int(n ** 0.5)

    if 'p_list' not in globals():
        p_list = primes(n_root * jumpahead)

    if p_list[-1] < n_root:
        p_list = primes(n_root * jumpahead)

    for p in p_list:
        if p > n_root:
            break

        if n % p == 0:
            return False

    return True


def totients(n):

    p_list = primes(n)

    p_set = set(primes(n))

    t_list = [0] + [1] * n

    for p in p_list:
        if p > n / 2:
            for k in range(p, n + 1):
                if t_list[k] == 1:
                    t_list[k] = k - 1
            break
        for i in range(p, n + 1, p):
            t_list[i] *= (p - 1)
        for x in range(2, int(log(n, p)) + 1):
            p_to_x = p ** x
            for j in range(p_to_x, n + 1, p_to_x):
                t_list[j] *= p
    return t_list


# Function for calculating a single totient (euler phi function), not using a prime list.
# Presumably not the fastest way to do this--really it should be crawling through all numbers by prime factorization.
# But still pretty fast.
def totient(n):

    if n == 1:
        return 1

    t = 1
    n_new = n
    n_root = int(n ** 0.5)
    for x in range(2, n_root + 1):
        if n_new % x == 0:
            power = 1
            n_new /= x
            while n_new % x == 0:
                power += 1
                n_new /= x
            t *= x ** (power - 1) * (x - 1)
        if n_new == 1:
            return t

    return t * (n_new - 1)


def relatively_prime_generator(n, f=lambda x: True, a=1, b=1):
    """Generates all relatively prime pairs x, y with x > y and x<= n.  The larger number comes first.
    f is an optional restriction that can be placed on each ordered pair"""
    if f((a, b)):
        yield (a, b)
    k = 1
    while a * k + b <= n:
        for i in relatively_prime_generator(n, f, a * k + b, a):
            if f(i):
                yield i
        k += 1


def at_least_one_even(tup):
    return tup[0] % 2 == 0 or tup[1] % 2 == 0


def pythagorean_triple_generator(c_max, primitive_only=False):
    for m, n in relatively_prime_generator(int(c_max ** 0.5), lambda x: x[0] % 2 == 0 or x[1] % 2 == 0):
        msq, nsq = m * m, n * n
        a, b, c = msq - nsq, 2 * m * n, msq + nsq
        if c <= c_max:
            yield a, b, c
        if not primitive_only:
            ka, kb, kc = a, b, c
            for _ in range(2, int(c_max / c) + 1):
                ka += a
                kb += b
                kc += c
                yield ka, kb, kc


def quadratic_eq(a, b, c):
    d = float(b**2 - 4 * a * c)
    if d < 0:
        raise Exception("No real solution to given quadratic equation")
    if d == 0:
        return -b / float(2 * a)
    else:
        return (-b - d ** 0.5) / float(2 * a), (-b + d ** 0.5) / float(2 * a)


def n_choose_k(n, k):
    return prod(range(n - k + 1, n + 1)) // prod(range(1, k + 1))


def get_all_factorizations(n):
    """
    Makes a list of prime factorizations up to and including n.
    The entry factorizations[315] would be the dictionary {3:2, 5:1, 7:1},
    corresponding to 3**2 * 5**1 * 7**1.
    The function goes through each prime p, first setting all multiples of p
    to include {p:1}, then incrementing all multiples of p**2, p**3, etc.
    """
    factorizations = [{} for _ in range(n + 1)]
    all_primes = primes(n)
    for p in all_primes:
        for q in range(p, n + 1, p):
            factorizations[q][p] = 1
        pow_limit = int(log(n, p))
        for x in range(2, pow_limit + 1):
            # Some redundancy in next line; we could just multiply previous power by p
            p_to_x = p ** x
            for r in range(p_to_x, n + 1, p_to_x):
                factorizations[r][p] += 1
    return factorizations