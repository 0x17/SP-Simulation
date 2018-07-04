#!/usr/bin/env python

import os

TIME_LIMIT = 1

instance_names = []
opt_profits = {}
with open('OptimalResults.txt', 'r') as fp:
    for line in fp.readlines()[1:]:
        parts = line.split(';')
        instance_name = parts[0].rstrip()
        opt_profit = float(parts[1].rstrip())
        opt_profits[instance_name] = opt_profit
        instance_names.append(instance_name)

instance_names.sort()

time_points = [ x / 100 for x in range(TIME_LIMIT*100) ]

def trace_files_for_instance(instance_name):
    return [ fn for fn in os.listdir('.') if fn.startswith(instance_name+'_') ]

def solver_name_from_trace_filename(trace_fn):
    return trace_fn.split('_')[1].replace('Trace.txt', '')

def clean_profit_str(ps): return ps.replace('-inf', '0.0')

traces = {}
for instance_name in instance_names:
    traces[instance_name] = {}
    for tfn in trace_files_for_instance(instance_name):
        slv = solver_name_from_trace_filename(tfn)
        if slv not in traces[instance_name]:
            traces[instance_name][slv] = []
        with open(tfn, 'r') as fp:
            for line in fp.readlines()[1:]:
                parts = line.split(';')
                traces[instance_name][slv].append((float(parts[0].rstrip()), float(clean_profit_str(parts[1].rstrip()))))

def best_profit_up_to(instance_name, slv, tp):
    bput = 0.0
    for tau,itsprofit in traces[instance_name][slv]:
        if tau <= tp and itsprofit > bput:
            bput = itsprofit
        if tau > tp: break
    return bput

def gap(obj, optimal_obj): return max(0.0, (optimal_obj-obj)/optimal_obj if optimal_obj > 0 else 0.0)

def avg(lst): return sum(lst) / len(lst)

ostr = 'time;Gurobi;LocalSolver;ParticleSwarm;FullEnumeration\n'

for tp in time_points:
    avggaps = []
    for slv in ['Gurobi', 'LocalSolver', 'ParticleSwarm', 'FullEnumeration']:
        gaps = []
        for instance_name in instance_names:
            optref = opt_profits[instance_name]
            bput = best_profit_up_to(instance_name, slv, tp)
            gaps.append(gap(bput, optref))
        avggaps.append(avg(gaps))
    avggapsstr = ';'.join([ '{:.4f}'.format(g) for g in avggaps])
    ostr += f'{str(tp)};{avggapsstr}\n'


with open('spmergedtraces.txt', 'w') as fp:
    fp.write(ostr)