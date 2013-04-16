#!python3

import sys
from read_counts import read_counts
from write_counts import write

def spatial_sum(counts, s):
    #where s = side length of new blocks
    N0 = len(counts[0])
    N1 = N0//s
    summed = [[0 for i in range(N1)] for j in range(N1)]

    for i, row in enumerate(counts):
        for j, elem in enumerate(row):
            summed[i//s][j//s] += elem

    return summed

def main():
    cts1 = read_counts(sys.argv[1])
    write(spatial_sum(cts1, 4), sys.argv[1].split('.')[0]+'_4x4')

if __name__ == "__main__":
    main()