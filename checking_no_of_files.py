import os
import glob

method_list = ['B3LYP']
basis_list = ['AUG-pcseg-2']

for lot in method_list:
     
    for bs in basis_list:
        
        log = 0
        pbs = 0
        gjf = 0
        chk = 0
        e = 0
        o = 0
        weird = 0
        
        path = f'/scratch/on41/na0696/PROJECT/input/{lot}/{bs}/*'
        paths = glob.glob(path)
        
        for file in paths:

            if file.endswith('.log') :

                log = log + 1

            elif file.endswith('.pbs') :

                pbs = pbs + 1

            elif file.endswith('.gjf') :

                gjf = gjf + 1

            elif file.endswith('.chk') :

                chk = chk + 1

            elif '.pbs.e' in file :

                e = e + 1

            elif '.pbs.o' in file :

                o = o + 1

            else :

                weird = weird + 1

        if log == gjf :

            print(f'{lot}/{bs} has correct number of output files :)')
                    
        print(f'For {lot}/{bs} :')
        print(log)
        print(pbs)
        print(gjf)
        print(chk)
        print(e)
        print(o)
        print(weird)

