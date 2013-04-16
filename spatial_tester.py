#!python3

from spatial_sum import spatial_sum
from read_counts import read_counts
from plot_counts import plot
from write_counts import write
import sys

def main():
    in_name = sys.argv[1]
    num = int(sys.argv[2])
    counts = read_counts(in_name)

    #s1: 2cm by 2cm detectors
    s1 = spatial_sum(counts, num)

    out_name = in_name.split('.')[0] + '_rad{}cm'.format(num*0.5)
    write(s1, out_name)
    plot(s1, out_name)

if __name__ == "__main__":
    main()