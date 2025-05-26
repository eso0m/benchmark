import pandas as pd
import glob
import io
import numpy as np

lots = ['M062X']
bss = ['6-31Gs', '6-31Gss', 'pcseg-1', 'AUG-pcseg-1', 'pcseg-2', 'AUG-pcseg-2', 'Def2SVP', 'Def2SVPD', 'cc-pVDZ', 'AUG-cc-pVDZ']

job_times_for_all_mcs = []

for lot in lots :

    for bs in bss :

        files = glob.glob(f'/scratch/on41/na0696/PROJECT/input/{lot}/{bs}/*.pbs.o*')
        job_times_per_mc = []
        job_times_per_mc_ints = []

        for file in files :
       
            job_time = []
            whole_line = []

            with open(file, 'r') as f:

                for line in f :

                    if 'Service Units:' in line :

                        for element in line :

                            whole_line.append(element)
            
            for n in whole_line :

                if n.isnumeric() :

                    job_time.append(n)

                elif n == '.' :

                    job_time.append(n)
            
            #if whole_line[-6].isnumeric() :

                #job_time.append(whole_line[-6])

            #job_time.append(whole_line[-5])
            #job_time.append(whole_line[-4])
            #job_time.append(whole_line[-3])
            #job_time.append(whole_line[-2])


            job_time_per_molecule = ''.join(job_time)
        
            job_times_per_mc.append(job_time_per_molecule)
            
        try :
            job_times_per_mc_ints = [eval(i) for i in job_times_per_mc]
            job_time_per_mc = np.sum(job_times_per_mc_ints)
            print(lot + ' ' + bs + ': ' + str(round((job_time_per_mc/1000), 4)) + ' kSU')

            job_times_for_all_mcs.append(job_time_per_mc)
        
        except : 

            print(lot + ' ' + bs)
