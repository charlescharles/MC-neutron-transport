def test(**kwargs):
    if 'den' in kwargs: print('den:{}'.format(kwargs['den']))
    if kwargs['mfp']: print('mfp:{}'.format(kwargs['mfp']))

if __name__ == "__main__":
    test(den=12.3, mfp=2.3)