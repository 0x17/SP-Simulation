import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import visalphapsi

S = 25
random.seed(23)
scenarios = [ random.randint(0, 50) for s in range(S) ]

alpha = 0.8
num_worst = round(S * (1-alpha))
worst = sorted(scenarios)[:num_worst]

olists = {}

def CVaR(ozero):
    omegaslist = [ 0 if s > ozero else ozero - s for s in scenarios ]
    if ozero not in olists: olists[ozero] = omegaslist #sorted(omegaslist)
    return ozero - 1.0 / ((1-alpha) * S) * sum(omegaslist)


xs = range(50)
cvars = [ CVaR(ozero) for ozero in range(50) ]

points = [ (x, cvars[x]) for x in range(10) ]
#print(points)

weight = 1.0 / ((1-alpha) * S)

six = 3
eix = 8

with PdfPages('omegazerofig.pdf') as pdf:
    # plt.plot(xs[six:eix], [ weight * x for x in xs ], label='weight')

    plt.xticks(np.arange(50))

    visalphapsi.plot_entries(scenarios, 'revenues', '', pdf)

    plt.plot(xs[six:eix], cvars[six:eix], label='CVaR', marker='o', linestyle='-.')
    plt.legend()
    pdf.savefig()

    plt.plot(xs[six:eix], xs[six:eix], label='ω0', marker='o', linestyle='-.')
    plt.legend()
    pdf.savefig()

    plt.plot(xs[six:eix], [sum(os > 0 for os in olists[x]) for x in xs][six:eix],
             label='#s:ωs>0 i.e. Gs<=ω0', marker='o', linestyle='-.')
    plt.legend()
    pdf.savefig()

    plt.plot(xs[six:eix], [sum(olists[x]) for x in xs][six:eix], label='ωs sum', marker='o', linestyle='-.')
    plt.legend()
    pdf.savefig()

    plt.plot(xs[six:eix], [1.0 / ((1 - alpha) * S) * sum(olists[x]) for x in xs][six:eix], label='ωs sum weighted', marker='o', linestyle='-.')
    plt.legend()
    pdf.savefig()

