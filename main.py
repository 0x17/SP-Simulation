import simulation
import evaluation
import helpers
import mipmodel

n_tries = 1000

def run_2d_plot():
	# sim = simulation.TwoClassSimulation('data.json')
	sim = simulation.TwoClassSimulation('data_normalized.json')
	evl = evaluation.Evaluator(sim)
	res = evl.collect_results(n_tries)
	evl.export_results_2d(res, 'simulation_results.xlsx')
	evl.plot_results_2d(res, show_opt=True)

def run_3d_plot():
	sim = simulation.MultiClassSimulation()
	evl = evaluation.Evaluator(sim)
	res = evl.collect_results(n_tries)
	evl.export_results_3d(res, 'simulation_results.txt')
	res = helpers.csv_file_to_tuple_list('simulation_results.txt', float)
	print(evl.compute_opt(res))
	evl.plot_results_3d(res)

def run_littlewood_example():
	sim = simulation.TwoClassSimulation('data_normalized.json')
	evl = evaluation.Evaluator(sim)
	evl.plot_littlewood_example()

def run_solver():
	#sim = simulation.TwoClassSimulation('data.json')
	#sim = simulation.TwoClassSimulation('data_normalized.json')
	sim = simulation.MultiClassSimulation()
	scenarios = sim.generate_scenarios(n_tries)
	mipmodel.solve(sim, scenarios)

def main():
	#run_littlewood_example()
	run_3d_plot()
	run_solver()

main()
