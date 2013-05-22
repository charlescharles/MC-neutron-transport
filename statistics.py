#!python3

import math, re, os
from bin import bin
from scipy import stats
from pylab import *


def chi_sq(template_cts, test_cts):
    'calculate chi-squared goodness-of-fit'
    chisq = 0
    for temp_row, test_row in zip(template_cts, test_cts):
        for temp_ct, test_ct in zip(temp_row, test_row):
            chisq += (temp_ct - test_ct)**2/(temp_ct+1.0)
    return chisq


def sensitivity(pval_thres, dev_thres):
    counts = {}
    devs = {}
    with open('processed_dim_variations_rad1.5', 'rU') as f:
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
    rads = []
    sens = []
    for rad in sorted(counts):
        rads.append(rad)
        #sens.append(devs[rad])
        sens.append(1.0*devs[rad]/counts[rad] if counts[rad] > 0 else -1)
        print(rad)
    plot(rads, sens)
    xlabel('radius (cm)')
    ylabel('sensitivity')
    xticks(list(range(1, 10)))
    grid(True)
    savefig("sens_vs_rad_rad15_cutoff_1.png")
    show()

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
    'Convert chi-squared values to probabilities, and calculate efficiencies'
    f = open('processed_dim_variations_dist50_detlen5', 'rU')
    f_out = open('dim_variation_results_dist50_detlen5_bkt{}'.format(bucket_size), 'w')
    counts = {}
    for line in f:
        rad, dof, deviation, chisq = [float(x) for x in line.split()]
        if rad not in counts:
            counts[rad] = [[], []]
        index = int(math.fabs(deviation)//bucket_size)
        if index >= len(counts[rad][0]):
            n = index - len(counts[rad][0]) + 1
            counts[rad][0].extend([0 for x in range(n)])
            counts[rad][1].extend([0 for x in range(n)])

        counts[rad][1][index] += 1  # counts[rad][1] = list representing the total counts
        pval = 1 - stats.chi2.cdf(chisq, dof)
        if pval <= thres: counts[rad][0][index] += 1  # counts[rad][0] = list representing deviated counts
        if pval >= thres:
            print('rad:{};deviation:{};pval:{}'.format(rad,deviation,pval))

    for rad in sorted(counts):
        for i, (dev, total) in enumerate(zip(counts[rad][0], counts[rad][1])):
            f_out.write('%.2f\t%.3f\t%.5f\n' % (rad, (i + 0.5)*bucket_size, (1.0*dev/total if total > 0 else 0)))
            #f_out.write('%.1f\t%.1f\t%.3f\n' % (rad, (i + 0.5)*bucket_size, dev))
    f_out.close()
    f.close()


def process_counts():
    'convert raw counts to chi squared values'
    #r = re.compile(r'sqdev([0-9.]+)_')
    r = re.compile(r'([-0-9.]+)_')

    # continue from where the previous session left off.
    # if no file exists, create one.
    distance = 50
    detlen = 5
    try:
        with open('processed_dim_variations_dist{0}_detlen{1}'.format(distance, detlen), 'r') as f:
            try:
                last = list(f)[-1]
                last_rad = float(last.split()[0])
            except IndexError:
                last_rad = 0.5
    except EnvironmentError:
        last_rad = 0.5

    radii = [i*0.5 for i in range(int(2*last_rad), 20)]
    files = os.listdir('dim_variations_rad1.5_dist{0}_detlen_{1}'.format(distance, detlen))
    for rad in radii:
        print('rad:{0}'.format(rad))
        template = bin('templates/dim_template_dist{0}_detlen_{1}'.format(distance, detlen), rad)
        n = len(template[0])
        for i in range(n):
            for j in range(n):
                template[i][j] /= 100.0
        # write and close one radius at a time.
        with open('processed_dim_variations_dist{0}_detlen{1}'.format(distance, detlen), 'a') as f_out:
            for fname in files:
                print(fname)
                deviation = r.search(fname).group(1)
                test = bin('dim_variations_rad1.5_dist{0}_detlen_{1}/'.format(distance, detlen) + fname, rad)
                dof = n**2 - 1

                f_out.write('{0}\t{1}\t{2}\t{3}\n'.format(rad, dof, deviation, chi_sq(template, test)))


if __name__ == '__main__':
    classify_chisq(0.05, 0.1)
