__author__ = 'raphey'

from random import randint

def random_matrix(r, c, b):
    rm = []
    for i in range(0, r):
        rm.append([])
        for j in range(0, c):
            rm[i].append(randint(0, b))
    return rm


def print_matrix(a):
    print "-------------------"
    for row in a:
        print row
    print "-------------------"


def identity(r, c=None):
    if c is None:
        c = r
    if c != r:
        print "Error: identity matrix needs to be square."
    eye = []
    for i in range(0, r):
        eye.append([0] * c)
        eye[i][i] = 1
    return eye


def ones(r, c=None):
    if c is None:
        c = r
    mat = []
    for i in range(0, r):
        mat.append([1] * c)
    return mat


def v_stack(mat1, mat2):
    if len(mat1[0]) != len(mat2[0]):
        print "Error: Matrices appear to have unequal widths."
    return mat1 + mat2


def h_stack(mat1, mat2):
    if len(mat1) != len(mat2):
        print "Error: Matrices appear to have unequal heights."
    stack = []
    for i in range(0, len(mat1)):
        stack.append(mat1[i] + mat2[i])
    return stack


def multiply(mat1, mat2):
    if len(mat1[0]) != len(mat2):
        print "Error--matrices' dimensions don't match."
        return
    product = []
    for i in range(0, len(mat1)):
        product.append([])
        for j in range(0, len(mat2[0])):
            product[i].append(0)
            for k in range(0, len(mat1[0])):
                product[i][j] += mat1[i][k] * mat2[k][j]
    return product


def multiply_mod(mat1, mat2, m):
    if len(mat1[0]) != len(mat2):
        print "Error--matrices' dimensions don't match."
        return
    product = []
    for i in range(0, len(mat1)):
        product.append([])
        for j in range(0, len(mat2[0])):
            product[i].append(0)
            for k in range(0, len(mat1[0])):
                product[i][j] += mat1[i][k] * mat2[k][j] % m
            product[i][j] %= m
    return product


def matrix_power(a, x):
    result = identity(len(a), len(a))
    while x > 0:
        if x % 2 == 1:
            result = multiply(result, a)
        a = multiply(a, a)
        x /= 2
    return result


def matrix_power_mod(a, x, m):
    result = identity(len(a), len(a))
    while x > 0:
        if x % 2 == 1:
            result = multiply_mod(result, a, m)
        a = multiply_mod(a, a, m)
        x /= 2
    return result