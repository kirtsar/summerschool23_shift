from sympy.combinatorics import Permutation, PermutationGroup
import numpy as np
import math
import sympy
import sympy.functions.combinatorial.numbers as math_num
from scipy.stats import chisquare
from scipy.stats import chi2


dict_cycles = {}
dict_points = {}

# {num of cycles: num of permutations}

# {num of cycles: num of permutation}

max_num = 10
num_of_perms = 2 ** 10

for i in range (num_of_perms):
    a = Permutation(np.random.permutation(max_num))
    cycle_num = a.cycles
    if cycle_num in dict_cycles.keys():
        dict_cycles[cycle_num] += 1
    else:
        dict_cycles[cycle_num] = 1

    # for cycle_len in cycles.keys():
    #     if cycle_len not in dict_cycles.keys():
    #         dict_cycles[cycle_len] = cycles[cycle_len]
    #     else:
    #         dict_cycles[cycle_len] += cycles[cycle_len]
list_keys = list(dict_cycles.keys())


f_exp_1 = [((1 / math.factorial(k)) * (sympy.subfactorial(max_num - k) / math.factorial(max_num -k))) for k in range(max_num)]
    
f_exp_cycles = [((1 / math.factorial(max(list_keys))) * math_num.stirling(max(list_keys), k, kind=1)) for k in range(1, max(list_keys) + 1)]

f_obs_cycles = np.array(list(dict_cycles.values()), dtype=float)

list_keys.sort()
dict_cycles = {i: dict_cycles[i] for i in list_keys}
f_exp_cycles = np.array([k * sum(f_obs_cycles) for k in f_exp_cycles], dtype=float)
dict_cycles.update((x, y) for x, y in dict_cycles.items()) 


s = sum(f_exp_cycles)
f_exp_cycles = [(i / s) for i in f_exp_cycles]
f_obs_cycles = [(i / s) for i in f_obs_cycles]
print(f_exp_cycles)
print(f_obs_cycles)

smth = chisquare(f_obs=f_obs_cycles, f_exp=f_exp_cycles)

# quantile = chi2.ppf(1-0.05, df=11)
# print(quantile)
print(smth[0], smth[1])