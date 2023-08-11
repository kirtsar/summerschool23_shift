import numpy as np
import operator
import sys

def generate_permutation_by_function(f):
    res = np.empty(2**N)
    for el in range(2**N):
        res[el] = f(el)
    return res


def create_operation(f, phi, psy, plus):
    def g(x, y):
        return f(plus(phi(x), psy(y)))
    return g


def left_shift_by_element(f, el):
    def g(x):
        return f(el, x)
    return g


def bijection(permutation):
    def f(x):
        return permutation[x]
    return f



# def E(*args, function):
#     def g(el):
#         res = el
#         for f in args:
#             res = 


N = 9
# f1, f2, f3 = bijection(np.random.permutation(2**N)), bijection(np.random.permutation(2**N)), bijection(np.random.permutation(2**N))
f1, f2, f3 = bijection(np.random.RandomState(seed=42).permutation(2**N)), bijection(np.random.RandomState(seed=43).permutation(2**N)), bijection(np.random.RandomState(seed=44).permutation(2**N))


np.set_printoptions(threshold=sys.maxsize)

a = 5
print(generate_permutation_by_function(left_shift_by_element(create_operation(f1, f2, f3, operator.xor), a)))
