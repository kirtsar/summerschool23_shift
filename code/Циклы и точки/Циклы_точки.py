#!/usr/bin/env python
# coding: utf-8

# In[178]:


from sympy.combinatorics import Permutation, PermutationGroup
import numpy as np
import math
import sympy
import sympy.functions.combinatorial.numbers as math_num
from scipy.stats import chisquare
from scipy.stats import chi2

# stat1, pvalue = chisquare(f_obs=num_of_cycles, f_exp=E_num_of_cycles)


# In[179]:


def conv(x):
    r = len(x) - 1
    last_sum = 0
    while (last_sum <= 5) & (r >= 0):
        last_sum += x[r]
        r = r - 1
    r += 1
    new_x = [0 for i in range(r+1)]
    for i in range(r):
        new_x[i] = x[i]
    new_x[r] = last_sum   
    while(new_x[0] == 0):
        new_x = new_x[1:]
    return new_x


# In[180]:


def chi(O, E):
    O = conv(O)
    E = conv(E)
    if len(O) != len(E):
        m = min(len(O), len(E)) 
        O = O[m:]
        E = E[m:]
    r = 0
    for i in range(len(O)):
        r += (O[i] - E[i])**2/E[i]
    return (r, len(O))


# In[181]:


n = 10  # длина подстановки
N = 2 ** 10 # размер выборки подстановок

num_of_cycles = [0 for k in range(n+1)]
num_of_fixed_points = [0 for k in range(n+1)]

a = Permutation(np.random.permutation(n))

for i in range(N):
    a = Permutation(np.random.permutation(n))
    cycle_num = a.cycles
    num_of_cycles[a.cycles] += 1
    if 1 in a.cycle_structure.keys():
        num_of_fixed_points[a.cycle_structure[1]]  += 1
    else:
        num_of_fixed_points[0] += 1
        
print(num_of_cycles)
print(num_of_fixed_points)


# In[182]:


# Неподвижные точки
E_prob_of_fixed_points = [((1 / math.factorial(k)) * (sympy.subfactorial(n - k) / math.factorial(n - k))) for k in range(n+1)]
E_num_of_fixed_points = [ x*N  for x in E_prob_of_fixed_points]
(num_of_fixed_points_stat, points_array_len) = chi(num_of_fixed_points, E_num_of_fixed_points)

#print(E_num_of_fixed_points)

points_quantile = chi2.ppf(1-0.05, df=points_array_len-1)

print("Квантиль степени " + str(points_array_len - 1) + " = " + str(points_quantile))
print("Статистика для k неподвижных точек = " + str(num_of_fixed_points_stat))


# In[183]:


# Длины циклов
E_prob_of_cycles = [((1 / math.factorial(n)) * math_num.stirling(n, k, kind=1)) for k in range(len(num_of_cycles))]
E_num_of_cycles = [ x*N  for x in E_prob_of_cycles]
(num_of_cycle_stat, cycle_array_len) = chi(num_of_cycles, E_num_of_cycles)

#print(E_num_of_cycles)

cycle_quantile = chi2.ppf(1-0.05, df=cycle_array_len-1)
print("Квантиль степени " + str(cycle_array_len - 1) + " = " + str(cycle_quantile))
print("Статистика для ровно k циклов = " + str(num_of_cycle_stat))

