#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:16:09 2021

@author: joshuaumiamaka
"""

try:
  from commands import getoutput
except:
  from subprocess import getoutput
import glob
import random
import time

for image in glob.glob('/home/tatumumi/supernova_lts/JWST_Vela/*/*/*/*/*f115w/*a0.[2-9]*_same_scale.fits'):
  f = open("sub.sh", 'w')
  f.write("#!/bin/bash\n")
  f.write("#SBATCH --job-name=example\n")
  f.write("#SBATCH --partition=shared\n")
  f.write("#SBATCH --time=0-00:05:00 ## time format is DD-HH:MM:SS\n")
  f.write("#SBATCH --nodes=1\n")
  f.write("#SBATCH --cpus-per-task=1\n")
  f.write("#SBATCH --mem=4G # Memory per node my job requires\n")
  f.write("#SBATCH --error=example-%A.err # %A - filled with jobid, where to write the stderr\n")
  f.write("#SBATCH --output=example-%A.out # %A - filled with jobid, wher to write the stdout\n")
  f.write("source ~/.bash_profile\n")
  f.write("cd /home/tatumumi/supernova_lts/JWST_Machine_Learning\n")
  f.write("python MachineLearningProjectFinal.py " + image)
  f.close()
  print(getoutput("sbatch sub.sh"))
  time.sleep(0.25)
  
  

    
  
