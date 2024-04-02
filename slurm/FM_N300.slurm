#!/bin/bash
####### Reserve computing resources #############
#SBATCH --job-name=FM_N300
#SBATCH --output=FM_N300.log
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
printf "\n The Runtime of dataset N300\n";
time python3.10 test_driver.py BE_NF_FM input/M2N300 rawdata/M2N300 300;
time python3.10 test_driver.py BE_NF_FM input/M4N300 rawdata/M4N300 300;
time python3.10 test_driver.py BE_NF_FM input/M6N300 rawdata/M6N300 300;
time python3.10 test_driver.py BE_NF_FM input/M8N300 rawdata/M8N300 300;
time python3.10 test_driver.py BE_NF_FM input/M10N300 rawdata/M10N300 300;
