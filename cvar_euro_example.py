import math
import numpy as np

np.random.seed(42)

J = 3
rj = [ 1 ] * 3
cj = [ 1, 2, 3 ]
C = 12

bin_nj = [12, 6, 4]
bin_pj = [0.25, 0.33, 0.6]

assert(len(rj) == len(cj) == len(bin_nj) == len(bin_pj) == J)

'''scenarios = [
    [6, 1, 5],
    [0, 0, 12],
    [0, 5, 12],
    [2, 3, 2],
]'''

def pick_demands(j): return np.random.binomial(bin_nj[j], bin_pj[j])
def pick_scenario(): return [ pick_demands(j) for j in range(J) ]

scenarios = [ pick_scenario() for s in range(150) ]

assert(all(len(scen) == J for scen in scenarios))

def djs(j, s): return scenarios[s][j]

def cumulative_consumption_from(j, nj):
    return sum(nj[i] * cj[i] for i in range(j+1, J))

def accept_vector(bcj, s):
    nj = [0] * J
    for j in reversed(range(J)):
        fitcount = math.floor((bcj[j] - cumulative_consumption_from(j, nj)) / cj[j])
        nj[j] = min(djs(j, s), fitcount)
    return nj

def revenue(bcj, s):
    return np.dot(accept_vector(bcj, s), rj)

def avg_revenue(bcj): return sum(revenue(bcj, s) for s in range(len(scenarios))) / len(scenarios)
def min_revenue(bcj): return min(revenue(bcj, s) for s in range(len(scenarios)))

def print_stats_for_bl(bcj):
    print(f'Booking limits = {bcj}')
    for s in range(len(scenarios)):
        print(f'Scenario {s}={scenarios[s]}, Accepts={accept_vector(bcj, s)}, Revenue={revenue(bcj, s)}')
    print(f'Average revenue = {avg_revenue(bcj)}, Minimum revenue = {min_revenue(bcj)}')

def full_enum(obj):
    best_obj = -1
    best_sol = [0]*J
    assert(J==3)
    b1 = C
    for b2 in range(0, b1+1):
        for b3 in range(0, b2+1):
            assert(b1 == C and b1 >= b2 >= b3 >= 0)
            bcj = [b1, b2, b3]
            o = obj(bcj)
            if o > best_obj:
                #print(f'Found new best known solution: {bcj} with obj = {o}')
                #if best_obj > 0: print(f'Improvement by {o-best_obj}')
                best_obj = o
                best_sol = bcj
    return best_sol, best_obj

print('Optimize for average')
sol, _ = full_enum(avg_revenue)
print_stats_for_bl(sol)

#print('Optimize for min')
#sol, _ = full_enum(min_revenue)
#print_stats_for_bl(sol)

#print_stats_for_bl([12, 10, 6])
#print_stats_for_bl([12, 12, 0])