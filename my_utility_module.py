__author__ = 'raphey'

# python 3

import time
import cProfile
from functools import update_wrapper, reduce


def read_2d_input(file_name, dtype=int, delimiter=','):
    data = []
    with open(file_name, "r") as f:
        content = f.readlines()
        for line in content:
            data.append(list(map(dtype, line.split(delimiter))))
    return data


def start_timer():
    global time0
    time0 = time.time()


def stop_timer():
    print("Time elapsed:", round(time.time() - time0, 3), "seconds")


def timed_call(fn, *args):
    """Call function with args; print the time in seconds.
    """
    t, result = timer(fn, *args)
    print("Time elapsed:", round(t, 3), "seconds")
    if result is not None:
        print("Result of function call:", result)


def timer(fn, *args):
    """Call function with args; return the time in seconds and result.
    """
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1 - t0, result


def average(numbers):
    """Return the average (arithmetic mean) of a sequence of numbers.
    """
    return sum(numbers) / float(len(numbers))


def timed_calls(n, fn, *args):
    """
    Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time
    """
    times = [timer(fn, *args)[0] for _ in range(n)]
    print("For %s calls of function, min time: %s \t avg time: %s \t max time: %s" %
          (n, round(min(times), 3), round(average(times), 3), round(max(times), 3)))


def time_profile(func_str):
    cProfile.run(func_str)


def decorator(d):
    """Make function d a decorator: d wraps a function fn."""
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f


def recursive_backtracking_search(state, is_goal, successors):
    solutions = []
    if is_goal(state):
        solutions.append(state)
    for succ_state in successors(state):
        solutions += recursive_backtracking_search(succ_state, is_goal, successors)
    return solutions


def function_tester(func, io_pairs):
    failed_tests = []
    for i, desired_o in io_pairs:
        try:
            actual_o = func(*i)
        except TypeError:
            actual_o = func(i)
        if actual_o != desired_o:
            failed_tests.append((i, actual_o, desired_o))
    print("Function {} passed {}/{} tests.".format(
        func.__name__, len(io_pairs) - len(failed_tests),
        len(io_pairs)))
    for (i, actual_o, desired_o) in failed_tests:
        print(" Failed test: {}({}) returned {}; expected {}.".format(
            func.__name__, i, actual_o, desired_o))


def prod(iter):
    return reduce(lambda x, y: x * y, iter, 1)