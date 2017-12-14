import matplotlib.pyplot as plt

sep = ';'

def parse_column(ix, lines):
    return [ float(line.split(sep)[ix].replace(',','.')) for line in lines ]

with open('mergedtraces.txt', 'r') as fp:
    lines = fp.readlines()
    header_parts = lines[0].split(sep)
    ncols = len(header_parts)
    labels = header_parts[1:]
    xs = parse_column(0, lines[1:])
    yslist = [ parse_column(i, lines[1:]) for i in range(1, ncols) ]
    for yctr in range(len(yslist)):
        plt.plot(xs, yslist[yctr], label=labels[yctr].replace('Trace,txt', ''))
    plt.legend()
    plt.savefig('mergedtraces.pdf')

