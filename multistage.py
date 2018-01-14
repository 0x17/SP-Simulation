import boxplots
import numpy as np
import matplotlib.pyplot as plt

obj = boxplots.json_from_file('multistage_data.json')

nscen = 150
demand_scenarios = [ [ np.random.poisson(client['expD']) for s in range(nscen) ] for client in obj['clients'] ]

#consumption_scenarios = ...

for ds in demand_scenarios:
    plt.hist(ds)

plt.show()