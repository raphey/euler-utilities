__author__ = 'raphey'


# Based on code from http://code.activestate.com/recipes/366178-a-fast-prime-number-list-generator/
def primes(n):

    if n < 2:
        return []

    primes_list = [2]                       # deals with 2 on its own
    s = list(range(3, n + 1, 2))            # list of odd numbers from 3 to n
    mroot = n ** 0.5                        # Reminder: this is a float
    # half = int((n + 1) / 2 - 1)             # This is just the length of s. Removed from original code to simplify
    i = 0                                   # Starting with i indexed to the first odd number in list s
    m = 3                                   # m will be all the prime numbers <= sqrt(N), starting with 3
    while m <= mroot:
        if s[i]:
            j = int((m * m - 3) / 2)             # This sets j such that s[j] is m^2. Funny indexing math.
            s[j] = 0                        # This sets the initial m^2 as not prime (this is the first value that
                                            # need be considered, since m times anything smaller than m will already
                                            # have been sieved out
            while j < len(s):               # Loop stops when we try to label a non-prime outside the range N
                s[j] = 0                    # Set a value to non-prime (seems to be redundant on first pass)
                j += m                      # Jump ahead by m in the odd number list, meaning 2m in actual numbers
                                            # For example, for m = 3, after marking 9 non-prime, marks 15, 21, 27...
                                            # Some numbers do get visited twice.
        i += 1                              # Move to next odd number index
        m = 2 * i + 3                       # Set m to the actual odd number in question
    primes_list.extend([x for x in s if x])
    return primes_list


def relatively_prime_generator(n, f=lambda x: True, a=1, b=1):
    """Generates all relatively prime pairs <= n.  The larger number comes first.
    f is an optional restriction that can be placed on the each ordered pair"""
    yield (a, b)
    k = 1
    while a * k + b <= n:
        for i in relatively_prime_generator(n, f, a * k + b, a):
            if f(i):
                yield i
        k += 1