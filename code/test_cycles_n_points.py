from sympy.combinatorics import Permutation, PermutationGroup
import numpy as np
import math
import sympy
import sympy.functions.combinatorial.numbers as math_num
from scipy.stats import chisquare
from scipy.stats import chi2


# {num of cycles: num of permutations}

max_num = 10
num_of_perms = 2 ** 10

dict_cycles = {}
dict_points = {}
dict_involutions = {}
perms = []

def theoretical_fixed_points(n: int, max_range_points: int):
    
    f_exp_points = [((1 / math.factorial(k)) * (sympy.subfactorial(n - k) / 
                    math.factorial(n -k))) for k in range(max_range_points)]
    
    return f_exp_points

def theoretical_cycles(n: int, max_range_cycles: int):
    f_exp_cycles = [((1 / math.factorial(n)) * math_num.stirling(n, k, kind=1)) for k in range(1, max_range_cycles + 1)]
    
    return f_exp_cycles

def theoretical_involutions(n: int, max_range_cycles: int):
    f_exp_involutions = [((1 / (math.sqrt(2 * math.sqrt(math.exp(1))))) * math.pow(n / math.exp(1), n / 2) *
                        math.pow(math.exp(1), math.sqrt(n))) for k in range(1)]

    return f_exp_involutions

def set_distributions(f_exp: np.array, f_obs: np.array):
    
    f_exp = np.array([k * sum(f_obs) for k in f_exp], dtype=float)
    if len(f_obs) < len(f_exp):
        f_exp = f_exp[:len(f_obs)]
    else:
        f_obs = f_obs[:len(f_exp)]

    so = sum(f_obs)
    se = sum(f_exp)

    f_exp = [(i / se) for i in f_exp]
    f_obs = [(i / so) for i in f_obs]

    return f_exp, f_obs

def add_to_dict(some_dict: dict, value):
    if value in some_dict.keys():
        some_dict[value] += 1
    else:
        some_dict[value] = 1
    

def generate_perms(max_num, num_of_perms):
    
    for _ in range (num_of_perms):
        a = Permutation(np.random.permutation(max_num))
        perms.append(a)
        
        cycle_num = a.cycles
        cycle_struct = a.cycle_structure
        fixed_points = cycle_struct[1] if 1 in cycle_struct.keys() else 0
        involutions = 1 if math.lcm(*cycle_struct.keys()) <= 2 else 0
        
        add_to_dict(dict_cycles, cycle_num)
        add_to_dict(dict_points, fixed_points)
        add_to_dict(dict_involutions, involutions)
        
    return perms, dict_cycles, dict_points, dict_involutions

def init_distributions(some_dict: dict, func_theor):
    
    list_keys = list(some_dict.keys())

    full_array = np.array([i for i in range(max_num)]) 
    for key in full_array:
        if key not in list_keys:
            some_dict[key] = 0

    list_keys = list(some_dict.keys())
    list_keys.sort()

    some_dict = {i: some_dict[i] for i in list_keys}
    some_dict.update((x, y) for x, y in some_dict.items())

    f_obs = np.array(list(some_dict.values()), dtype=float)

    f_exp = func_theor(max_num, max(list_keys))

    return f_obs, f_exp

def check_random_parameter(f_obs, f_exp, alpha: float, df: int):
    
    stat = chisquare(f_obs=f_obs, f_exp=f_exp)[0]
    quantile = chi2.ppf(alpha, df=df)

    print("Theoretical: ", quantile)
    print(": ", stat)

    return stat < quantile

def main():

    perms, dict_cycles, dict_points, dict_involutions = generate_perms(max_num, num_of_perms)

    f_obs_cycles, f_exp_cycles = init_distributions(dict_cycles, theoretical_cycles)
    f_obs_points, f_exp_points = init_distributions(dict_points, theoretical_fixed_points)
    # f_obs_involutions, f_exp_involutions = init_distributions(dict_involutions, theoretical_involutions)

    f_exp_cycles, f_obs_cycles = set_distributions(f_exp_cycles, f_obs_cycles)
    f_exp_points, f_obs_points = set_distributions(f_exp_points, f_obs_points)
    # f_exp_involutions, f_obs_involutions = set_distributions(f_exp_involutions, f_obs_involutions)

    print(f_obs_involutions)
    print(f_exp_involutions)


    print(check_random_parameter(f_obs_cycles, f_exp_cycles, 0.05, max_num - 1) 
          and check_random_parameter(f_obs_points, f_exp_points, 0.05, max_num - 1))

    # print(abs((f_obs_involutions[1] - f_exp_involutions[0])) / max_num)



if __name__ == '__main__':
    main()
