import os
import sys
sys.path.append(os.environ['GUROBI_HOME'] + '\\python35\\lib')

from gurobipy import *
import gurobipy
import numpy as np
import math
import sys

def solve(sim, dsj):
    def printStatus(objVal, bcj, njs, rcapjs, kjs):
        print('Obj val = ', objVal)
        for j in range(len(sim.customers)):
            print('customer', str(j), '.consumption=', sim.customers[j].consumptionPerReq)
            #print('Optimal booking limit for class ', str(i + 1), ' = ', bcj[i].x / sim.customers[i].consumptionPerReq, ' (in request units)')
            print('Optimal booking limit for class ', str(j + 1), ' = ', bcj[j].x, ' (in capacity units)')
            #print('Optimal reserved for class ', str(i + 1), ' = ', (sim.C - bcj[i].x) / sim.customers[i].consumptionPerReq,' (in request units)')
            #print('Optimal reserved for class ', str(i + 1), ' = ', sim.C - bcj[i].x, ' (in capacity units)')

            '''

            for s in range(len(dsj)):
                print('s=', str(s), ', kjs=', kjs[j, s].x)
                print('s=', str(s), ', rcapjs=', rcapjs[j,s].x)
                print('s=', str(s), ', ncjs=', ncjs[j,s].x)
                print('s=', str(s), ', djs=', dsj[s][j])
            print()
            '''


    try:
        model = Model("serviceportfolios")

        # sets
        J = range(sim.num_classes)
        S = range(len(dsj))

        # parameters
        def cj(j): return int(sim.customers[j].consumptionPerReq)
        def rj(j): return int(sim.customers[j].revenuePerReq)

        # primary decision variables
        bcj = [model.addVar(vtype=GRB.INTEGER, name='bc' + str(j), lb=(sim.C if j == 0 else 0), ub=sim.C) for j in J]
        # derived variables
        njs = np.matrix([[model.addVar(vtype=GRB.CONTINUOUS, name='nc' + str(j) + ',' + str(s), lb=0, ub=math.floor(sim.C / cj(j))) for s in S] for j in J])
        rcapjs = np.matrix([[ model.addVar(vtype=GRB.CONTINUOUS, name='rc' + str(j) + ',' + str(s), lb=0, ub=sim.C) for s in S ] for j in J ])
        kjs = np.matrix([[model.addVar(vtype=GRB.INTEGER, name='kjs' + str(j) + str(s), lb=0, ub=math.floor(sim.C / cj(j))) for s in S ] for j in J])

        # objective
        model.setObjective(1 / len(S) * quicksum([ njs[j, s] * rj(j) for j in J for s in S]), GRB.MAXIMIZE)
        # constraints
        for j in J:
            if j + 1 < len(J):
                model.addConstr(bcj[j] >= bcj[j+1], 'monotonically_decreasing_booking_limits' + str(j))

            for s in S:
                model.addConstr(kjs[j, s] * cj(j) <= rcapjs[j, s], 'remaining_order_booking_limit' + str(j) + ',' + str(s))
                model.addConstr(kjs[j,s] * cj(j) >= rcapjs[j, s] - cj(j) + 1, 'remaining_order_booking_limit' + str(j) + ',' + str(s))
                model.addConstr(rcapjs[j,s] == (bcj[j] - quicksum([ njs[i,s] * cj(i) for i in range(j+1, sim.num_classes) ])), 'remaining_total_of_limit' + str(j) + ',' + str(s))
                model.addGenConstrMin(njs[j, s], [ kjs[j,s] ], dsj[s][j], 'combine_remaining_limit_demand' + str(j) + ',' + str(s))

        model.update()
        model.optimize()

        printStatus(model.objVal, bcj, njs, rcapjs, kjs)

    except GurobiError as e:
        print(e)
