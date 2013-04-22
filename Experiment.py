from Simulation import Simulation, Target, write

def template():
    tungsten_ring = Target(sig=5.45, den=15.8, mass=183.8, descr='tungsten_ring')
    sim = Simulation(target=tungsten_ring, runs=int(1e6), det_len=8, bank_size=50)

def density():
    mfp_list = [1.0, 1.5, 2, 2.5, 3, 3.25, 3.4, 3.54, 3.7, 4.0]
    for mfp_test in mfp_list:
        for i in range(10):
            tgt = Target(mfp=mfp_test, mass=183.8, descr='tungsten_ring_den{0}'.format(str(mfp_test)))
            sim = Simulation(target=tgt, runs=int(1e5), det_len=8, bank_size=50)
            distr = sim.distr
            out_name = '/u/cguo/SpringJP/density_tests/' + str(sim) + '_run{0}.counts'.format(i)
            write(out_name, distr)

if __name__ == "__main__":
    density()