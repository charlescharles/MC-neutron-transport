#!python3

from read_counts import read_counts
from plot_counts import plot
import math, sys

def confidence_highlighter(template_file, test_file):
    template = read_counts(template_file)
    test = read_counts(test_file)
    N = len(template[0])
    stdevs = [[0 for i in range(N)] for j in range(N)]

    for i in range(N):
        for j in range(N):
            if template[i][j] == 0:
                stdevs[i][j] = math.sqrt(test[i][j])
            else:
                stdevs[i][j] = (test[i][j]-template[i][j]*1.0)/math.sqrt(template[i][j])

    #print("expected anomalies: " + str(N*N*(1-0.997)))
    sig = 3.5
    #plot(stdevs, threshold=sig, fname='no_div_spread_div_{}sigma'.format(sig))
    plot(stdevs, threshold=True, fname='f2')

if __name__ == "__main__":
    confidence_highlighter(sys.argv[1], sys.argv[2])