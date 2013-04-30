from Simulation import Simulation, Target, write
import random, sys
random.seed()


def find_mfp(sig, den, mass):
    return mass/((6.022*10**23)*den*sig*(10**-24))


def template():
    #tungsten
    sig1 = 3  # barns, for elastic scattering
    den1 = 19.25  # g/cc
    mass1 = 183.84  # amu
    mfp1 = find_mfp(sig1, den1, mass1)

    #aluminum
    sig2 = 0.7  # barns, for elastic scattering
    den2 = 2.7  # g/cc
    mass2 = 26.98  # amu
    mfp2 = find_mfp(sig2, den2, mass2)

    template_obj = Target(mfp1=mfp1, mfp2=mfp2, r1=3.0, r2=7.0, r3=10.0, m1=mass1, m2=mass2, descr='template_obj')
    sim = Simulation(target=template_obj, runs=int(1e5), det_len=8, bank_size=50)

    '''
    tungsten_ring = Target(sig=5.45, den=15.8, mass=183.8, descr='tungsten_ring')
    sim = Simulation(target=tungsten_ring, runs=int(1e5), det_len=8, bank_size=50)
    distr = sim.distr
    '''

    out_name = str(sim) + '.counts'
    distr = sim.distr
    write(out_name, distr)


def density():
    mfp_list = [1.0, 1.5, 2, 2.5, 3, 3.25, 3.4, 3.54, 3.7, 4.0]
    for mfp_test in mfp_list:
        for i in range(10):
            tgt = Target(mfp=mfp_test, mass=183.8, descr='tungsten_ring_den{0}'.format(str(mfp_test)))
            sim = Simulation(target=tgt, runs=int(1e5), det_len=8, bank_size=50)
            distr = sim.distr
            out_name = '/u/cguo/SpringJP/mfp_tests/' + str(sim) + '_run{0}.counts'.format(i)
            write(out_name, distr)


def dim_template():
    template = Target(5.286, 23.705, 0, descr='dim_template_rad1.5')
    sim = Simulation(template, runs=int(1e7), det_len=8, bank_size=50)
    out_name = '/u/cguo/SpringJP/templates/dim_template'
    write(out_name, sim.distr)


def dim_variations(num):
    for i in range(num):
        x1 = random.uniform(-7, 7)
        tgt = Target(5.286, 23.705, x1, descr=('%.4f' % x1))
        sim = Simulation(target=tgt, runs=int(1e5), det_len=8, bank_size=50)
        #out_name = str(sim)
        out_name = '/u/cguo/SpringJP/dim_variations_rad1.5/' + str(sim)
        write(out_name, sim.distr)

def random_target():
    r1 = random.uniform(2, 4)
    r2 = random.uniform(6, 8)
    r3 = 10

    mfp1 = random.uniform(0.8*5.286, 1.2*5.286)
    mfp2 = random.uniform(0.8*23.705, 1.2*23.705)

    r1, r2, r3 
    norm_tgt_vec = [r1/10.0, r2/10.0, (mfp1 - 0.5*5.286)/(5.286),
                    (mfp2 - 0.5*23.705)/23.705]
    norm_template_vec = [3/10.0, 7/10.0, 0.5, 0.5]
    assert len(norm_template_vec) == len(norm_tgt_vec)
    sq_deviation = sum([(x - y)**2 for x, y in zip(norm_tgt_vec, norm_template_vec)])

    return [mfp1, mfp2, r1, r2, r3, 'sqdev{0}'.format(sq_deviation)]


def variations(num):
    for i in range(num):
        tgt = Target(*random_target())
        sim = Simulation(target=tgt, runs=int(1e5), det_len=8, bank_size=50)
        #out_name = 'variations/' + str(sim)
        out_name = '/u/cguo/SpringJP/variations/' + str(sim)
        write(out_name, sim.distr)


if __name__ == "__main__":
    if sys.argv[1] == 'template': dim_template()
    else: dim_variations(int(sys.argv[1]))
