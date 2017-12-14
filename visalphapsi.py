import json
import os
import sys
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


def plot_coords_from_entries(entries):
    frequencies = {}
    for entry in entries:
        frequencies[entry] = 1 if entry not in frequencies else frequencies[entry] + 1

    for k in range(max(frequencies.values()) + 1):
        if k not in frequencies:
            frequencies[k] = 0

    freq_sorted = OrderedDict(sorted(frequencies.items()))

    xs, ys = [], []
    for k, v in freq_sorted.items():
        xs.append(k)
        ys.append(v)

    return xs, ys

def plot_frequencies_for_class(i, instance_data, data, outfn, pdf):
    class_name = data['header'][i+1]
    xs, ys = plot_coords_from_entries([ int(row[1 + i]) for row in data['rows'] ])
    fig, ax = plt.subplots()
    client = instance_data['clients'][i]
    caption = class_name+' demand, μ=' + str(client['expD']) + ', σ=' + str(client['devD'])
    ax.bar(xs, ys, 0.3, label=caption)
    ax.legend(loc='best')
    if pdf is None:
        plt.savefig(outfn)
    else:
        #plt.title(caption)
        pdf.savefig()

def basename_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]

def read_scenarios(instance_data, fn):
    with open(fn, 'r') as fp:
        data = json.load(fp)
        with PdfPages(basename_from_path(fn)+'.pdf') as pdf:
            for i in range(3):
                outfn = basename_from_path(fn) + 'plotClass' + str(i+1) + '.pdf'
                plot_frequencies_for_class(i, instance_data, data, outfn, pdf)

def plot_entries(entries, caption, fn, pdf = None):
    print(f"Plotting entries {caption}")
    xs, ys = plot_coords_from_entries(entries)
    fig, ax = plt.subplots()
    ax.bar(xs, ys, 0.3, label=caption)
    ax.legend(loc='best')
    if pdf is None:
        plt.savefig(basename_from_path(fn) + caption + '.pdf')
    else:
        #plt.title(caption)
        pdf.savefig()
    plt.close()

def read_alpha_psi_variations(fn):
    with open(fn, 'r') as fp:
        data = json.load(fp)
        plot_entries([float(row[2]) for row in data['rows']], 'Profits', fn)
        with PdfPages(basename_from_path(fn)+'BookingLimits.pdf') as pdf:
            for i in range(3):
                plot_entries([ float(row[3+i]) for row in data['rows'] ], 'booking limits j'+str(i+1), fn, pdf)

def scenario_revenues_for_alpha_psi(alpha, psi, basepath):
    fn = basepath + 'psi' + str(psi) + '_alpha' + str(alpha) + '_profits.json'
    with open(fn, 'r') as fp:
        data = json.load(fp)
        return [ float(row[1]) for row in data['rows'] ]


def average_profit_worst_percent(alpha, psi, basepath, perc):
    revenues = scenario_revenues_for_alpha_psi(alpha, psi, basepath)
    num_worst = round(len(revenues) * perc)
    return np.average(sorted(revenues)[:num_worst])

def stddev_of_revenues(alpha, psi, basepath):
    revenues = scenario_revenues_for_alpha_psi(alpha, psi, basepath)
    return np.std(revenues)


def read_psi_alpha_profits(alpha, psi, basepath, pdf):
    fn = basepath + 'psi' + str(psi) + '_alpha' + str(alpha) + '_profits.json'
    plot_entries(scenario_revenues_for_alpha_psi(alpha, psi, basepath), 'scenario revenues α='+str(round(alpha*0.1, 2))+' ψ='+str(round(psi*0.1,2)), fn, pdf)

def persist_csv_for_alpha_psi(callback, basepath, outfn):
    ostr = 'table;' + ';'.join([str(round(i * 0.1, 2)) for i in range(11)]) + '\n'
    for alphactr in range(11):
        ostr += str(round(alphactr * 0.1, 2)) + ';' + ';'.join([str(callback(alphactr, psictr, basepath)) for psictr in range(11)]) + '\n'
    with open(outfn, 'w') as fp:
        fp.write(ostr.replace('.', ','))

def build_additional_tables(basepath):
    persist_csv_for_alpha_psi(lambda alpha, psi, basepath: average_profit_worst_percent(alpha, psi, basepath, 0.5), basepath, 'worst50Percent.csv')
    persist_csv_for_alpha_psi(stddev_of_revenues, basepath, 'stddevprofits.csv')

REL_PATH = '../CPP-Simulation/'
SCENARIO_FILENAMES = [ 'scenarios.json', 'scenariosDescriptive.json' ]
INST_FN = 'multi_data_cvar.json'

def main(args):
    with open(REL_PATH + INST_FN, 'r') as fp:
        instance_data = json.load(fp)
        for scenario_fn in SCENARIO_FILENAMES:
            read_scenarios(instance_data, REL_PATH + scenario_fn)

    read_alpha_psi_variations(REL_PATH + 'alphaPsiVariations.json')

    with PdfPages('psialphaprofits.pdf') as pdf:
        for psictr in range(11):
            for alphactr in range(11):
                read_psi_alpha_profits(alphactr, psictr, REL_PATH, pdf)

    build_additional_tables(REL_PATH)

if __name__ == '__main__':
    main(sys.argv)
