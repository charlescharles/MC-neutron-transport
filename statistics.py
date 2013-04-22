import math
from bin import bin
from scipy.stats import chi2

def chi_sq(template_cts, test_cts):
    'calculated chi-squared goodness-of-fit'
    chisq = 0
    for temp_row, test_row in zip(template_cts, test_cts):
        for temp_ct, test_ct in zip(temp_row, test_row):
            chisq += (temp_ct - test_ct)**2/(temp_ct+1.0)
    return chisq

def is_deviation(template_cts, test_cts, thres):
    'classify as the same or not the same based on chi-squared goodness-of-fit test'
    chisq = chi_sq(template_cts, test_cts)
    dof = (len(template_cts[0]))**2 - 1
    pval = 1 - chi2.cdf(chisq, dof)
    if pval <= thres: return True
    else: return False

def efficiencies(rad):
    mfp_list = [1.0, 1.5, 2, 2.5, 3, 3.25, 3.4, 3.54, 3.7, 4.0]
    template = bin('counts/tungsten_ring_runs1000000_detlen8_size50.counts', rad)
    n = len(template[0])
    for i in range(n):
        for j in range(n):
            template[i][j] /= 10
    eps = []
    for mfp in mfp_list:
        eff = 0
        for i in range(10):
            fname = 'counts/density_tests/tungsten_ring_den{0}_runs100000_detlen8_size50_run{1}.counts'.format(str(mfp), str(i))
            test = bin(fname, rad)
            if is_deviation(template, test, 0.05): eff += 1
        eps.append(eff)
    return eps

if __name__ == "__main__":
    radii = [i*0.5 for i in range(1, 14)]
    f_out = open('eff_vs_mfp', 'w')
    for rad in radii:
        print('r = {0}'.format(rad) + str(efficiencies(rad)))
        f_out.write('r = {0}'.format(rad) + str(efficiencies(rad)) + '\n')
    f_out.close()