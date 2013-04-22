#!python3

import sys, re, math
from plot_counts import *

def bin(fname, radius):
    'bins counts into cylindrical detectors'
    diam = 2.0*radius
    r = re.compile(r'_size([0-9]+)')
    d = float(r.search(fname).group(1))
    '''
    if 1.0*d%diam != 0:
        print('diameter not divisible into detector side length.')
        print('detector side length: {0}'.format(d))
        raise Exception('detector ({0}) indivisible by diameter ({1})!'.format(d, diam))
        return
    '''

    #n = the number of detectors on a side
    n = int(d/diam)
    counts = [[0 for i in range(n)] for j in range(n)]
    f = open(fname, 'rU')
    for line in f:
        parts = line.split()
        (x, y) = (float(parts[0]), float(parts[1]))
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