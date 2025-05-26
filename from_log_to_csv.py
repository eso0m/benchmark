# libraries used

import glob
import pandas as pd
import os
import shutil
import subprocess

# defining functions

def make_lot_directory(lot) :
    
    if not os.path.exists(f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}/') :
        
        os.mkdir(f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}')
        
def make_lot_bs_directory(lot, bs) :

    if not os.path.exists(f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}/{bs}') :

        os.mkdir(f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}/{bs}')
        
def naming(file) :
    
    filen = file.split('/')[-1].split('_')[0]

    if '_1_' in file :

        filen = filen + '_1'

    return filen

def error_check(type, int, line) :

    if type == 'successful' :

        if 'Normal termination' in line :
                   
            int = int + 1
    
    elif type == 'symmetry' :

        if 'ERROR: ' in line :

            int = int + 1

    elif type == 'termination' :

        if 'Error termination' in line :

            int = int + 1

    return int

def anharmonic(output_file) :
    
    all_freqs_data, all_freqs_desc, all_ints_data, anharmonic_data, fundamentals_data, overtones_data, combands_data = [], [], [], [], [], [], []
    copy = False # to avoid random lines
    
    for line in output_file:
        
        if 'Integrated intensity (I) in km.mol^-1' in line.strip():

            copy = True
            
        elif 'Units: Transition energies (E) in cm^-1' in line.strip():

            copy = False
            
        elif copy:
            
            anharmonic_data.append(line)
    
    # remove unnecessary blank spaces and characters.

    anharmonic_data = list(filter(lambda line: not line.startswith(' -'), anharmonic_data))
    anharmonic_data = list(filter(lambda line: not line.startswith('\n'), anharmonic_data))

    # FUNDAMENTALS FREQUENCY DATA
    
    for row in anharmonic_data:

        row = row.strip()
        
        if 'Fundamental Bands' in row:
    
            copy = True

        elif 'Overtones' in row:

            copy = False

        elif copy:
          
            fundamentals_data.append(row.split())
    
    fundamentals_data.pop(0)
    
    # append relevant data from fundamentals frequencies (frequencies, intensities and description)
    
    for line_freqs in fundamentals_data:

        all_freqs_data.append(line_freqs[1])
        all_freqs_data.append(line_freqs[2])

        all_ints_data.append(line_freqs[3])
        all_ints_data.append(line_freqs[4])

        all_freqs_desc.append('Harmonic')
        all_freqs_desc.append('Fundamental')

    # OVERTONES FREQUENCY DATA

    for row in anharmonic_data:

        row = row.strip()

        if 'Overtones' in row:

            copy = True

        elif 'Combination Bands' in row:

            copy = False

        elif copy:

            overtones_data.append(row.split())

    overtones_data.pop(0)

    # append relevant data from overtone frequencies (frequencies, intensities and description)

    for line_info in overtones_data:

        all_freqs_data.append(line_info[2])
        all_ints_data.append(line_info[3])
        all_freqs_desc.append('Overtone')
    
    # COMBINATION BANDS FREQUENCY DATA

    copy = False

    for row in anharmonic_data:

        row = row.strip()

        if 'Combination Bands' in row:

            copy = True

        elif 'GradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGrad' in row:

            copy = False

        elif copy:

            combands_data.append(row.split())

    if combands_data != []:

        combands_data.pop(0)
    
    # append relevant data from combination bands frequencies (frequencies, intensities and description)
     
    for line_info in combands_data:
        
        all_freqs_data.append(line_info[3])    
        all_ints_data.append(line_info[4])
        all_freqs_desc.append('CombBand')

    freq_dict = dict(zip(all_freqs_data,all_freqs_desc))

    return all_freqs_data,all_freqs_desc,all_ints_data

def error_printout(type, file, lot, bs, filen, failed_df) :

    print(file.split('/')[-1] + ' has ' + type)
    
    row_info = list([lot,bs,filen,type])
    failed_df.loc[len(failed_df.index)] = row_info
    
    shutil.copy(file.split('.')[0] + '.gjf', f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}/{bs}')
    shutil.copy(file.split('.')[0] + '.pbs', f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}/{bs}')
    
    return failed_df

# from log to csv

method_list = ['B3LYP']
basis_list = ['AUG-cc-pVDZ']

for lot in method_list : # for each lot

    make_lot_directory(lot) # make lot directory if it doesn't exist

    for bs in basis_list : # and each bs
        
        make_lot_bs_directory(lot, bs) # make bs directory if it doesn't exist
        
        files_names = glob.glob(f'/scratch/on41/na0696/PROJECT/input/{lot}/{bs}/C3O2_B3LYP_AUG-cc-pVDZ.log')
         
        anh_df = pd.DataFrame(columns = ['Formula','Frequencies','Freq_Kind','Intensities',])
        failed_df = pd.DataFrame(columns = ['LoT', 'BS', 'molecule', 'type of error',])
        
        for file in files_names :
            
            filen = naming(file)
            
            with open(file, 'r') as output_file : # open each individual output file and the benchmark dataset as reference for the SMILES codes

                    successful_calc, symmetry_error, termination_error = (0,)*3 
                    
                    for line in output_file :

                        successful_calc = error_check('successful', successful_calc, line) # check for successful files
                        symmetry_error = error_check('symmetry', symmetry_error, line) # check for symmetry error
                        termination_error = error_check('termination', termination_error, line) # check for termination error
                        
                    if successful_calc >= 2 : # continue for output files that terminated normally (they must have 2 'Normal termination')
                        
                        with open(file) as output_file:
                                                       
                            all_freqs_data, all_freqs_desc, all_ints_data = anharmonic(output_file)

                            neg_freqs = 0
                            asterisk_freqs = 0

                            for freq in all_freqs_data : # test for errors (imaginary frequencies, *****, symmetry and termination)

                                if '**********' in freq :

                                    asterisk_freqs = asterisk_freqs + 1

                                elif float(freq) < 0 :

                                    neg_freqs = neg_freqs + 1

                            if neg_freqs == 0 and asterisk_freqs == 0 : # if no errors, print data into a dataframe (later csv file)
                                
                                row_info = list([filen,all_freqs_data,all_freqs_desc,all_ints_data])
                                anh_df.loc[len(anh_df.index)] = row_info
                            
                            else : # if errors found, print the name of the molecule and print data into spearate dataframe (later csv file)

                                if neg_freqs > 0 :
                                
                                    error_printout('imaginary frequencies', file, lot, bs, filen, failed_df)

                                elif asterisk_freqs > 0 :
                                    
                                    error_printout('*****', file, lot, bs, filen, failed_df)

                                else :
                                
                                    error_printout('unknown error (terminated correctly)', file, lot, bs, filen, failed_df)

                    else :
                        
                        if symmetry_error > 0 :

                            error_printout('symmetry error', file, lot, bs, filen, failed_df)

                        elif termination_error > 0 :

                            error_printout('termination error', file, lot, bs, filen, failed_df)
        
                        else :

                            error_printout('unknown error (terminated incorrectly)', file, lot, bs, filen, failed_df)

        name = f'{lot}_{bs}.csv'
       
        anh_df.to_csv(os.path.join('/scratch/on41/na0696/PROJECT/output/run1', name)) # save output csv
        failed_df.to_csv(os.path.join(f'/scratch/on41/na0696/PROJECT/failed/run1/{lot}/{bs}', name)) # save failed csv
