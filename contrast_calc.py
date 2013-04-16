#!python3
from read_counts import read_counts
import sys

def contrast_calc(counts):
    N = len(counts[0])
    total_counts = sum([sum(row) for row in counts])
    mean = total_counts/(N*N)
    sum_squares = sum([sum([(elem - mean)**2 for elem in row]) for row in counts])
    rms_contrast = (sum_squares**0.5)/(N*N)
    return rms_contrast

def main():
    counts = read_counts(sys.argv[1])
    print(contrast_calc(counts))

if __name__ == "__main__":
    main()