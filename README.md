# benchmark
Code used in my anharmonic frequency benchmark project from Y4 of my MChem degree.

The aim of the project was to analyse anharmonic vibrational frequency data calculated using approximate computational models and compare it to its harmonic counterparts. The analysis was focused on 3 main aspects: accuracy of the obtained data compared to the experimental results, time required to compute the data and reliability of the used models.

More detailed description on how to use the provided code:

PART 1 (preparation)
1. Prepare .gjf and .pbs files for running calculations on GADI. (prepare_files.ipynb)
2. Convert .log output files obtained from GADI into .csv files. (from_log_to_csv.py)
3. Run additional file and computer time check on GADI. (checking_no_of_files.py and computer_time.py)

PART 2 (analysis)
1. Run reliability and timings analysis using generated .csv files. (reliability.ipynb and timings.ipynb; this step requires .csv output files for all models, as well as timings_report.csv generated manually)
3. Analyse types of errors that result in unreliable models. (error_types.ipynb)
4. Combine run 1 and 2 for hybrids. (fusing_csvs.ipynb)
5. Copy over the double hybrids data from run 1 into 'final' folder.
6. Order data by level of theory. Run the code for both harmonic and anharmonic frequencies, and all band types. (order_data_by_lot.ipynb)
7. Run harmonic vs anharmonic comparison code. (harm_anharm_comparison.ipynb)
8. Analyse outliers. (outliers.ipynb)
9. Run accuracy analysis. (accuracy.ipynb)
