#!python3

import math, re, os
from bin import bin
from scipy import stats


def chi_sq(template_cts, test_cts):
    'calculate chi-squared goodness-of-fit'
    chisq = 0
    for temp_row, test_row in zip(template_cts, test_cts):
        for temp_ct, test_ct in zip(temp_row, test_row):
            chisq += (temp_ct - test_ct)**2/(temp_ct+1.0)
    return chisq


def classification_power(pval_thres, dev_thres):
    counts = {}
    devs = {}
    with open('chisq_variations', 'rU') as f:
        for line in f:
            rad, dof, deviation, chisq = [float(x) for x in line.split()]
            if deviation >= dev_thres:
                if rad not in counts:
                    counts[rad] = 0
                    devs[rad] = 0

                counts[rad] += 1  # counts[rad][1] = list representing the total counts
                pval = 1 - stats.chi2.cdf(chisq, dof)
                if pval <= pval_thres:
                    devs[rad] += 1
    with open('sensitivities', 'w') as f:
        for rad in sorted(counts):
            f.write('%.2f\t%.4f\n' % (rad, 1.0*devs[rad]/counts[rad] if counts[rad] > 0 else -1))

    counts = {}
    devs = {}
    with open('chisq_variations', 'rU') as f:
        for line in f:
            rad, dof, deviation, chisq = [float(x) for x in line.split()]
            if deviation <= dev_thres:
                if rad not in counts:
                    counts[rad] = 0
                    devs[rad] = 0

                counts[rad] += 1  # counts[rad][1] = list representing the total counts
                pval = 1 - stats.chi2.cdf(chisq, dof)
                if pval <= pval_thres:
                    devs[rad] += 1
    with open('specificities', 'w') as f:
        for rad in sorted(counts):
            f.write('%.2f\t%.4f\n' % (rad, 1.0*devs[rad]/counts[rad] if counts[rad] > 0 else -1))


def classify_chisq(thres, bucket_size):
    f = open('chisq_variations', 'rU')
    f_out = open('variation_results', 'w')
    counts = {}
    for line in f:
        rad, dof, deviation, chisq = [float(x) for x in line.split()]
        if rad not in counts:
            counts[rad] = [[], []]
        index = int(deviation//bucket_size)
        if index >= len(counts[rad][0]):
            n = index - len(counts[rad][0]) + 1
            counts[rad][0].extend([0 for x in range(n)])
            counts[rad][1].extend([0 for x in range(n)])
        print('index:{}'.format(index))

        counts[rad][1][index] += 1  # counts[rad][1] = list representing the total counts
        pval = 1 - stats.chi2.cdf(chisq, dof)
        if pval <= thres: counts[rad][0][index] += 1  # counts[rad][0] = list representing deviated counts

    for rad in sorted(counts):
        for i, (dev, total) in enumerate(zip(counts[rad][0], counts[rad][1])):
            f_out.write('%.2f\t%.5f\t%.9f\n' % (rad, (i + 0.5)*bucket_size, (1.0*dev/total if total > 0 else 0)))
            #f_out.write('%.1f\t%.1f\t%.3f\n' % (rad, (i + 0.5)*bucket_size, dev))
    f_out.close()
    f.close()


if __name__ == '__main__':
    #classify_chisq(0.05, 0.01)
    classification_power(0.05, 0.003)
