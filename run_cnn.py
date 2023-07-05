#!/bin/bash
#SBATCH --job-name=example
#SBATCH --partition=shared
#SBATCH --time=0-16:00:00 ## time format is DD-HH:MM:SS
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=6G # Memory per node my job requires
#SBATCH --error=example-%A.err # %A - filled with jobid, where to write the stderr
#SBATCH --output=example-%A.out # %A - filled with jobid, wher to write the stdout
source ~/.bash_profile
cd /home/tatumumi/supernova_lts/JWST_Machine_Learning
python cnn_real.py
