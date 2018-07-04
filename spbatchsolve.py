#!/usr/bin/env python

import os

def syscall(s):
    print('SYSCALL: ' + s)
    os.system(s)

def os_command_str(cmd):
    return './' + cmd + ' ' if os.name == 'posix' else cmd + '.exe '

solvers = ['Gurobi', 'LocalSolver', 'ParticleSwarm', 'FullEnumeration']

def myrename(src,dest):
    print(f'Rename {src} to {dest}!')
    os.rename(src, dest)

def files_with_ext(dir, ext): return map(lambda ifn2: (dir + '/' + ifn2).replace('.json', ''), filter(lambda ifn: ifn.endswith(ext), os.listdir(dir)))

def compute_optimals():
    for fn in files_with_ext('Instances', '.json'):
        syscall(os_command_str('CPP-Simulation') + f'instance={fn} solver=Gurobi nscenarios=150 timelimit=9999.0 trace=false')
    myrename('GurobiResults.txt', 'OptimalResults.txt')

def compute_traces():
    for fn in files_with_ext('Instances', '.json'):
        instance_name = os.path.splitext(os.path.basename(fn))[0]
        for slv in solvers:
            syscall(os_command_str('CPP-Simulation') + f'instance={fn} solver={slv} nscenarios=150 timelimit=5.0 trace=true')
            myrename(f'{slv}Trace.txt', f'{instance_name}_{slv}Trace.txt')

def cleanup():
    os.remove('spmergedtraces.txt')
    for fn in [ fn for fn in os.listdir('.') if fn.endswith('Trace.txt') or (fn.endswith('Results.txt') and not(fn == 'OptimalResults.txt')) ]:
        os.remove(fn)

compute_optimals()
#compute_traces()
#cleanup()