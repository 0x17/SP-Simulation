import random
import math
import scipy.stats

class ObjectFromJson:
	def __init__(self, **entries):
		self.__dict__.update(entries)

def slurp(fn):
	with open(fn) as f:
		return f.read()

def pick_rand_std_normal():
	u1 = random.uniform(0, 1)
	u2 = random.uniform(0, 1)
	return math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)

def pick_normal(mean, stddev):
	return round(mean + stddev * pick_rand_std_normal(), 0)

def inv_normal(x, mean, stddev):
	return stddev * scipy.stats.norm.ppf(x) + mean

def tuple_column_averages(tuples):
	return list(map(lambda s: s / len(tuples), map(sum, zip(*tuples))))

def list_average(lst):
	return sum(lst) / float(len(lst))

def extract_column(tuples, ix):
	return list(map(lambda tuple: tuple[ix], tuples))

def tuple_list_to_csv_file(header_tuple, tuples, filename):
	def tuple_to_csv_line(tpl):
		csv_line = ''
		for ix in range(len(tpl)):
			sep = ';' if ix + 1 < len(tpl) else '\n'
			csv_line += str(tpl[ix]) + sep
		return csv_line

	with open(filename, 'w') as f:
		tuple_to_csv_line(header_tuple)
		for tpl in tuples:
			f.write(tuple_to_csv_line(tpl))

def csv_file_to_tuple_list(filename, converter):
	tuples = []
	with open(filename, 'r') as f:
		lines = f.readlines()[1:]
		for line in lines:
			parts = line.split(';')
			tuples.append(tuple(map(lambda part: converter(part), parts)))
	return tuples

def dist_func(expD, devD, x):
	return scipy.stats.norm.cdf(x, loc=expD, scale=devD)