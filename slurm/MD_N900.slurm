#!/bin/bash
####### Reserve computing resources #############
#SBATCH --job-name=MD_N900
#SBATCH --output=MD_N900.log
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
printf "\n The Runtime of dataset N900\n";
time python3.10 test_driver.py BE_NF_MD input/M2N900 rawdata/M2N900 300;
time python3.10 test_driver.py BE_NF_MD input/M4N900 rawdata/M4N900 300;
time python3.10 test_driver.py BE_NF_MD input/M6N900 rawdata/M6N900 300;
time python3.10 test_driver.py BE_NF_MD input/M8N900 rawdata/M8N900 300;
time python3.10 test_driver.py BE_NF_MD input/M10N900 rawdata/M10N900 300;
