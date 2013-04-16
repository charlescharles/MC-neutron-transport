#!python3

from spatial_sum import spatial_sum
from read_counts import read_counts
from plot_counts import plot
from write_counts import write
from diff import diff
import sys

def main():
    in1 = sys.argv[1]
    in2 = sys.argv[2]
    counts1 = read_counts(in1)
    counts2 = read_counts(in2)

    diffs = diff(counts1, counts2)
    out_name = "{}_{}_diff".format(in1.split('.')[0], in2.split('.')[0])
    write(diffs, out_name)
    plot(diffs, out_name)

if __name__ == "__main__":
    main()