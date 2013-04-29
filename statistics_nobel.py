#!python3

import math, re, os
from bin import bin
#from scipy import stats

def chi_sq(template_cts, test_cts):
    'calculate chi-squared goodness-of-fit'
    chisq = 0
    for temp_row, test_row in zip(template_cts, test_cts):
        for temp_ct, test_ct in zip(temp_row, test_row):
            chisq += (temp_ct - test_ct)**2/(temp_ct+1.0)
    return chisq

'''
def is_deviation(template_cts, test_cts, thres):
    'classify as the same or not the same based on chi-squared goodness-of-fit test'
    chisq = chi_sq(template_cts, test_cts)
    dof = (len(template_cts[0]))**2 - 1
    pval = 1 - stats.chi2.cdf(chisq, dof)
    if pval <= thres: return True
    else: return False
'''

def efficiencies(rad):
    mfp_list = [2.0+0.1*i for i in range(21)]
    template = bin('tungsten_ring_runs1000000_detlen8_size50.counts', rad)
    n = len(template[0])
    for i in range(n):
        for j in range(n):
            template[i][j] /= 10
    f_out = open('mfp_chisquared', 'w')
    for mfp in mfp_list:
        for i in range(50):
            fname = 'mfp_tests/tungsten_ring_den{0}_runs100000_detlen8_size50_run{1}.counts'.format(str(mfp), str(i))
            test = bin(fname, rad)
            f_out.write('{}\t{}\t{}\n'.format(mfp, i, chisq(template, test)))


def process_counts():
    'convert raw counts to chi squared values'
    r = re.compile(r'sqdev([0-9.]+)_')

    # continue from where the previous session left off.
    # if no file exists, create one.
    try:
        with open('chisq_variations', 'r') as f:
            try:
                last = list(f)[-1]
                last_rad = float(last.split()[0])
            except IndexError:
                last_rad = 0.5
    except EnvironmentError:
        last_rad = 0.5

    radii = [i*0.5 for i in range(int(2*last_rad), 20)]
    files = os.listdir('variations')
    for rad in radii:
        print('rad:{0}'.format(rad))
        template = bin('templates/template_obj_runs10000000_detlen8_size50.counts', rad)
        n = len(template[0])
        for i in range(n):
            for j in range(n):
                template[i][j] /= 100
        files = os.listdir('variations')
        # write and close one radius at a time.
        with open('chisq_variations', 'a') as f_out:
            for fname in files:
                deviation = r.search(fname).group(1)
                test = bin('variations/' + fname, rad)
                dof = n**2 - 1

                f_out.write('{0}\t{1}\t{2}\t{3}\n'.format(rad, dof, deviation, chi_sq(template, test)))


'''
if __name__ == "__main__":
    radii = [i*0.5 for i in range(1, 14)]
    f_out = open('eff_vs_mfp', 'w')
    for rad in radii:
        print('r = {0}'.format(rad) + str(efficiencies(rad)))
        f_out.write('r = {0}'.format(rad) + str(efficiencies(rad)) + '\n')
    f_out.close()
'''

if __name__ == '__main__':
    process_counts()