import json

tblkeys = [ 'expD', 'devD', 'revenuePerReq', 'consumptionPerReq' ]

with open('../CPP-Simulation/multi_data_big.json', 'r') as fp:
    obj = json.load(fp)
    ostr = '$C=' + str(obj['capacity']) + '$, und \\begin{tabular}{|c|c|c|c|c|}\n'
    ostr += '\\hline\nj & $\mu_j$ & $\sigma_j$ & $r_j$ & $c_j$\\\\\n\\hline\n'
    clients = obj['clients']
    ts = ' & '
    for j in range(len(clients)):
        client = clients[j]
        ostr += str(j+1) + ts + ts.join([str(client[k]) for k in tblkeys ]) + '\\\\\n\hline\n'
    ostr += '\end{tabular}\n'
    with open('multi_data_big.tex', 'w') as fp2:
        fp2.write(ostr)
        print(ostr)

