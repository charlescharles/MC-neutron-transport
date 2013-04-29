import random
random.seed()

if __name__ == '__main__':
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
    print(sq_deviation)