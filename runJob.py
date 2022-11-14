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
from astropy.io import fits
import tqdm


def get_number_of_jobs():
  return len(getoutput("squeue | grep $USER").split('\n'))

files_made = glob.glob("file-home*F115W*fits")
#files_made = [item.replace("F115W", "f115w") for item in files_made]

for image in tqdm.tqdm(glob.glob('/home/tatumumi/supernova_lts/JWST_Vela/*/*/*/*/*f115w/*a0.[2-9]*_same_scale.fits')):
  output_image_name = "file" + image.replace("/", "-").replace("f115w", "F115W")
  run_this_image = False

  if files_made.count(output_image_name) == 0:
    run_this_image = True
    print("Couldn't find ", output_image_name, "rerunning")
  else:
    try:
      for filt in ["F115W", "F150W", "F277W", "F444W"]:
        f = fits.open(output_image_name.replace("F115W", filt))
        f.close()
        print("opened ", output_image_name.replace("F115W", filt), "okay")

      run_this_image = False # output_image_name exists, and it's a valid fits file
    except:
      print("Found ", output_image_name, "but there was a problem opening it")
      run_this_image = True

  
  if run_this_image:
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

    while get_number_of_jobs() > 50:
      print("Too many jobs. Checking again soon.")
      time.sleep(3.)

    print(getoutput("sbatch sub.sh"))
    time.sleep(0.25)
  
