from plot_counts import plot
from read_counts import read_counts
import sys


if __name__ == '__main__':
    cts = read_counts(sys.argv[1])
    plot(cts, fname='templateobj')
