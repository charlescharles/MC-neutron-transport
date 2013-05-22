from Simulation import Simulation, Target, write
import random, sys
random.seed()


def template():
    distance = 50
    detlen = 5
    template = Target(5.286, 23.705, 0, dist=distance)
    sim = Simulation(template, runs=int(1e7), det_len=detlen, bank_size=50, dist=distance)
    out_name = '/u/cguo/SpringJP/templates/dim_template_dist{0}_detlen_{1}'.format(distance, detlen)
    write(out_name, sim.distr)


def geometry_variations(num):
    distance = 50
    detlen = 5
    for i in range(num):
        x1 = random.uniform(-7, 7)
        tgt = Target(5.286, 23.705, x1, dist=distance, descr=('%.4f_%d' % (x1, distance)))
        sim = Simulation(target=tgt, runs=int(1e5), det_len=detlen, bank_size=50, dist=distance)
        out_name = '/u/cguo/SpringJP/dim_variations_rad1.5_dist{0}_detlen_{1}/{2}'.format(distance, detlen, sim)
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
    if sys.argv[1] == 'template': template()
    else: geometry_variations(int(sys.argv[1]))
