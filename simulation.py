import json

from sympy.ntheory import residue_ntheory

import helpers
import random
import math

class AbstractSimulation:
	def __init__(self, data_fn):
		obj = json.loads(helpers.slurp(data_fn))
		self.customers = tuple(map(lambda client: helpers.ObjectFromJson(**client), obj['clients']))
		self.C = obj['capacity']
		self.num_classes = len(self.customers)

	def pick_demands(self):
		return tuple(map(lambda customer: max(0, helpers.pick_normal(customer.expD, customer.devD)), self.customers))

	def generate_scenarios(self, n_tries):
		random.seed(42)
		s = list(map(lambda i: self.pick_demands(), range(n_tries)))
		return s

	def run_simulation(self, booking_limits, scenarios):
		return list(map(lambda scenario: self.objective(scenario, booking_limits), scenarios))

class TwoClassSimulation(AbstractSimulation):
	def __init__(self, data_fn):
		AbstractSimulation.__init__(self, data_fn)

	def objective(self, demands, b2):
		reserved_1 = self.C - b2
		booking_limit_1 = self.C
		n2 = math.floor(min(b2, demands[1] * self.customers[1].consumptionPerReq) / self.customers[1].consumptionPerReq)
		n1 = math.floor(min(demands[0] * self.customers[0].consumptionPerReq, self.C - n2 * self.customers[1].consumptionPerReq, booking_limit_1) / self.customers[0].consumptionPerReq)
		profit = n1 * self.customers[0].revenuePerReq + n2 * self.customers[1].revenuePerReq
		return n1, n2, profit

	def optimal_policy(self):
		r1 = self.customers[0].revenuePerReq
		r2 = self.customers[1].revenuePerReq
		x = (r1 - r2) / r1
		return math.floor(self.customers[0].consumptionPerReq * helpers.inv_normal(x, self.customers[0].expD, self.customers[0].devD))

class MultiClassSimulation(AbstractSimulation):
	def __init__(self):
		AbstractSimulation.__init__(self, 'multi_data.json')

	def objective(self, demands, booking_limits):
		residual_capacity = self.C
		profit = 0.0
		for ix in reversed(range(self.num_classes)):
			u = min(demands[ix], math.floor( (booking_limits[ix] - (self.C - residual_capacity)) / self.customers[ix].consumptionPerReq ) )
			residual_capacity -= u * self.customers[ix].consumptionPerReq
			profit += u * self.customers[ix].revenuePerReq
		return profit