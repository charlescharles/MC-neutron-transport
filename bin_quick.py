from bin import bin
from Simulation import write
import os

if __name__ == '__main__':
    fname = [f for f in os.listdir('./templates/') if f.startswith('template_')][0]
    counts = bin('templates/' + fname, 0.5)
    out_name = 'binned_template_counts'
    n = len(counts)
    with open(out_name, 'w') as f:
        for i in range(n):
            for j in range(n):
                f.write('{0}\t{1}\t{2}\n'.format(i, j, counts[i][j]))
