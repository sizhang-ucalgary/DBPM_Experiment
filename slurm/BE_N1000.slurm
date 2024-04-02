#!/bin/bash
####### Reserve computing resources #############
#SBATCH --job-name=BE_N1000
#SBATCH --output=BE_N1000.log
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
printf "\n The Runtime of dataset N1000\n";
time python3.10 test_driver.py BE input/M2N1000 rawdata/M2N1000 300;
time python3.10 test_driver.py BE input/M4N1000 rawdata/M4N1000 300;
time python3.10 test_driver.py BE input/M6N1000 rawdata/M6N1000 300;
time python3.10 test_driver.py BE input/M8N1000 rawdata/M8N1000 300;
time python3.10 test_driver.py BE input/M10N1000 rawdata/M10N1000 300;
