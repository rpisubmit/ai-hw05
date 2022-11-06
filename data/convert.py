import os
import subprocess
import tqdm
import shutil

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    faces = subprocess.run("find faces -name '*.pgm' | grep -ve '[24].pgm' | sort", check=True, shell=True, capture_output=True).stdout.decode().split('\n')
    faces = [a for a in faces if a != '']
    # this will sort faces so we have them ordered by individual
    faces_sorted = sorted(faces)
    l = len(faces_sorted)
    _e1 = int(l * 0.8)
    _e2 = int(l * 0.9)
    train = faces_sorted[:_e1]
    val = faces_sorted[_e1:_e2]
    test = faces_sorted[_e2:]
    print ([len(a) for a in [train, val, test]])
    for s, p in zip([train, val, test], ['pngs/train', 'pngs/validation', 'pngs/test']):
        outp = f'{path}/{p}'
        print (f'deleting existing {outp}')
        shutil.rmtree(outp, ignore_errors=True)
        subd1 = 'sunglasses'
        subd2 = 'open'
        for subd in [subd1, subd2]:
            os.makedirs(f'{outp}/{subd}')
        print (f'creating {outp} data')
        for f in tqdm.tqdm(s):
            base = os.path.basename(f).rsplit('.')[-2]
            subd = subd1 if 'sunglasses' in base else subd2
            p = f'{outp}/{subd}/{base}' 
            subprocess.run(['convert', f, f'{outp}/{subd}/{base}.png'], check=True, capture_output=True)


if __name__ == '__main__':
    main()
