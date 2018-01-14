import matplotlib.pyplot as plt
import json
import numpy as np
import itertools
import sys

def json_from_file(fn):
    with open(fn, 'r') as fp:
        return json.load(fp)

def parse_scenarios(fn):
    data = json_from_file(fn)
    return { data['header'][1+i]: [ int(row[1+i]) for row in data['rows'] ] for i in range(3) }

def truncate_and_round(nums):
    return [ max(0, round(num)) for num in nums ]

def main(args):
    relpath = '../CPP-Simulation/'

    regular_scenarios = parse_scenarios(relpath + 'scenarios.json')
    descriptive_scenarios = parse_scenarios(relpath + 'scenariosDescriptive.json')

    class_keys = ['j1', 'j2', 'j3']

    clients = json_from_file(relpath + 'multi_data_cvar.json')['clients']

    distributions = {
    'j' + str(j + 1): truncate_and_round(np.random.normal(clients[j]['expD'], clients[j]['devD'], 1000000)) for j in
    range(3)}


    def combined_scenarios(dict):
        return [dict[k] for k in class_keys]


    def scenarios_for_class(classname):
        return [regular_scenarios[classname], descriptive_scenarios[classname], distributions[classname]]

    labels = ['reg ' + ck for ck in class_keys] + ['descr' + ck for ck in class_keys] + ['act' + ck for ck in
                                                                                         class_keys]
    labels_reordered = [classname + ' ' + dtype for classname, dtype in
                        itertools.product(class_keys, ['reg', 'descr', 'act'])]

    data = []
    for classname in class_keys:
        data += scenarios_for_class(classname)

    plt.boxplot(data, labels=labels_reordered, showfliers=False)
    #plt.show()
    plt.savefig('boxplots.pdf')

if __name__ == '__main__':
    main(sys.argv)
