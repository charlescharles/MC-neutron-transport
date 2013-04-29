#!python3

import sys, re, math
from plot_counts import *

def bin(fname, radius):
    'bins counts into cylindrical detectors'
    diam = 2.0*radius
    r = re.compile(r'_size([0-9]+)')
    try:
        d = float(r.search(fname).group(1))
    except AttributeError:
        d = 50
    #n = the number of detectors on a side
    n = int(d/diam)
    counts = [[0 for i in range(n)] for j in range(n)]
    f = open(fname, 'rU')
    for line in f:
        parts = line.split()
        try:
            (x, y) = (float(parts[0]), float(parts[1]))
        except (ValueError, IOError):
            continue
        (x, y) = (x + d/2, d/2 - y)
        #now the bottomleft corner is at (0,0) and topright is (n,n)
        # after flipping across x-axis and shifting up d/2 and right d/2
        (i, j) = (int(x//diam), int(y//diam))
        #print('x:{}; y:{}; i:{}; j:{}'.format(float(parts[0]), float(parts[1]),i,j))
        (x0, y0) = (i*diam+radius, j*diam+radius)
        if math.sqrt((x-x0)**2 + (y-y0)**2)<=radius:
            try: counts[i][j] += 1
            except IndexError: pass
    f.close()
    return counts

if __name__ == "__main__":
    arglen = len(sys.argv)
    if arglen < 3:
        print("usage:\n\t'python bin '[filename.counts]' [detector-radius]'")
    else:
        counts = bin(sys.argv[1], float(sys.argv[2]))
        plot(counts)
        total = 0
        for row in counts:
            print('{}\n'.format(row))
            total += sum(row)
        print('avg count = {}'.format(total/(len(counts[0])**2)))