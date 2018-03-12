__author__ = 'raphey'
# Python 2

from fractions import Fraction
from math import factorial


# Function to fit a degree d polynomial to data. y_list and x_list lists of coordinates of length d + 1, with x_list as
# an arithmetic series. Returns a list of rational coefficients for the polynomial.
def series_poly_fit(y_list, x_list):
    s = x_list[1] - x_list[0]       # Step size for arithmetic series
    d = len(y_list) - 1
    poly = []
    working_y_list = y_list[:]
    new_poly_coeff = 0
    for i in range(0, d + 1):  # Each time through this loop adds one term to the polynomial coefficient list
        delta = highest_order_delta(working_y_list)
        curr_d = d - i
        new_poly_coeff = Fraction(delta, (s ** curr_d) * factorial(curr_d))
        poly.append(new_poly_coeff)
        working_y_list = modify_ys(working_y_list[:len(y_list) - i - 1], x_list, new_poly_coeff, curr_d)

    return poly


# Function to return the highest order delta for a series of polynomial function outputs from an arithmetic series of x
# values.
def highest_order_delta(vals):
    while len(vals) > 1:
        vals = [vals[x] - vals[x - 1] for x in range(1, len(vals))]
    return vals[0]


# Returns a y_list modified according to the coefficients of a polynomial that have been found thus far.
def old_modify_ys(y_list, x_list, poly, d):
    if len(poly) == 0:
        return y_list
    new_y_list = y_list[:]
    for i in range(0, len(new_y_list)):
        for j in range(0, len(poly)):
            new_y_list[i] -= poly[j] * x_list[i] ** (d - j)
    return new_y_list


# Returns a y_list modified by subtracting a new polynomial term with coefficient coeff and degree d.
def modify_ys(y_list, x_list, coeff, d):
    new_y_list = y_list[:]
    for i in range(0, len(new_y_list)):
        new_y_list[i] -= coeff * x_list[i] ** d
    return new_y_list