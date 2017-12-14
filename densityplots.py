import sys

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import special

import numpy as np

my_customer = { 'expD': 20.0, 'consumptionPerReqMean': 40.0 }

def eos_consumption(customer, u):
    delta_x = customer['expD']
    delta_y = customer['consumptionPerReqMean'] * 0.2
    return max(1.0, customer['consumptionPerReqMean'] - (special.erf(4 * u / delta_x - 2) * delta_y / 2.0 + delta_y / 2.0))

def plot_normpdf(x, mu, sigma, label):
    plt.plot(x, mlab.normpdf(x, mu, sigma), label=label)

def plot_eos_consumptions(domain):
    plt.plot(domain, [ eos_consumption(my_customer, u) for u in domain ])

TEX_NEWLINE = '\\\\\n'
TEX_HLINE = '\hline' + TEX_NEWLINE

def expand(val, num_digits):
    return ('%.'+str(num_digits)+'f') % round(val, num_digits)

def table_row_from_dict(column_names, dict):
    return ' & '.join([ str(dict[column_name]) if column_name == 'u' else expand(dict[column_name], 2) for column_name in column_names ])

def dparams_to_tex(dist_params):
    ostr = '\\begin{tabular}{|r|cc|}\n\\hline\n'
    ostr += '$u$ & $\\mu_{\Gamma_j}(u)$ & $\\sigma_{\Gamma_j}(u)$' + TEX_NEWLINE + '\\hline\n'
    ostr += TEX_NEWLINE.join([ table_row_from_dict(['u', 'mu', 'sigma'], dp) for dp in dist_params ])
    ostr += TEX_NEWLINE+'\\hline\n\\end{tabular}'
    return ostr


def plot_pdfs(udomain, plotdomain):
    def mu(u): return eos_consumption(my_customer, u)
    def sigma(u): return mu(u) / 10

    dist_params = [{'mu': mu(u), 'sigma': sigma(u), 'u': u} for u in udomain]
    print(dparams_to_tex(dist_params))

    x = np.linspace(plotdomain[0], plotdomain[1], 100)

    for dparams in dist_params:
        plot_normpdf(x, dparams['mu'], dparams['sigma'], 'u=' + str(dparams['u']))

def main(args):
    #plot_eos_consumptions(range(1, 30, 2))
    plot_pdfs(range(1, 31, 4), (20, 60))
    plt.legend(loc='best')
    plt.show()
    #plt.savefig('GlockenSkalen.pdf')

if __name__ == '__main__':
    main(sys.argv)
