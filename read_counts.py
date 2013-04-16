#!python3

import sys

def read_counts(filename):
    f = open(filename, 'r')
    counts = []
    for line in f:
        i, j, ct = (int(x) for x in line.split())
        if j == 0: counts.append([])
        counts[i].append(ct)
    f.close()
    return counts