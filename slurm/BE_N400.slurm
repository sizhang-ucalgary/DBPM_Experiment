#!/bin/bash
####### Reserve computing resources #############
#SBATCH --job-name=BE_N400
#SBATCH --output=BE_N400.log
#
#SBATCH --partition=bigmem
#SBATCH --exclude=mmg1,mmg2
#SBATCH --time=1-00:00:00
#SBATCH --mem=256gb
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#
#SBATCH --mail-user=si.zhang2@ucalgary.ca
#SBATCH --mail-type=end,fail

####### Set environment variables ###############
module load python/3.10.4 

####### Run your script #########################
printf "\n The Runtime of dataset N400\n";
time python3.10 test_driver.py BE input/M2N400 rawdata/M2N400 300;
time python3.10 test_driver.py BE input/M4N400 rawdata/M4N400 300;
time python3.10 test_driver.py BE input/M6N400 rawdata/M6N400 300;
time python3.10 test_driver.py BE input/M8N400 rawdata/M8N400 300;
time python3.10 test_driver.py BE input/M10N400 rawdata/M10N400 300;
