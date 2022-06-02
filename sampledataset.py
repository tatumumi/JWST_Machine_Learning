#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 11:46:28 2022

@author: joshuaumiamaka
"""

import glob
import os.path
import subprocess
from astropy.io import fits
import pickle
import tqdm


all_images = []
sup_img = []
filt = ["f115w","f150w","f277w","f444w"]

#method to check if supernova places 16 pixels within border
def check_bound():
    if i >= 16 and i <= length - 16 and j >= 16 and j <= length -16:
        bound = 1
    else: 
        bound = 0
    return bound
    
 #method to crop image into 32 x 32   
def crop32():
    all_data_for_SN.append(h[0].data[i-16:i+16, j-16:j+16]*1.)
    return all_data_for_SN

#method to crop image into 16 x 16
def crop16():
    all_data_for_SN.append(h[0].data[i-8:i+8, j-8:j+8]*1.)
    return all_data_for_SN
    
def image_count():
    count = len(all_images)
    return count
    
check115 = False
check150 = False
check277 = False
check444 = False

for image in tqdm.tqdm(glob.glob('file-home-**.fits')):
        #subprocess.getoutput("/Applications/ds9 new_file_" + filter + ".fits")
        #open each of the four images 
        
        print(image)
        
        #checks if 115W exists
        if os.path.exists(image) == True:
            check115 = True
        else:
            check115  = False
            
        #checks if 150W exists
        if os.path.exists(image.replace("f115w", "f150w")) == True:
            check150 = True
        else:
            check150 = False
            
        #checks if 277W exists
        if os.path.exists(image.replace("f115w", "f277w")) == True:
            check277 = True
        else:
            check277 = False
            
        #checks if 444W exists
        if os.path.exists(image.replace("f115w", "f444w")) == True:
            check444 = True
        else:
            check444 = False
        
        
        if check115 & check150 & check277 & check444 == True:
        #for exists(image.replace(filt,"f150w"))
               print("all checks")
             
               k = 0
               while k < len(filt):
                   h = fits.open(image.replace("f115w", filt[k]))        
                   data = h[0].data
                   length = len(data)
                   header = h[0].header
                   all_data_for_SN = []
                   bound = 0
                   i = header["SN_i"]
                   j = header["SN_j"]
                   #check if supernova was planted
                   if h[0].header["placed"] == 'yes':
                      supernova = 1
                    #adds image with nova into array
                      sup_img.append(image)
                   else:
                          supernova = 0
                            #add filter adjustments for crop
                   if supernova == 1:
                        h.checkbound(i,j)
                        if bound == 1:
                            all_data_for_SN = crop32() 
                        else:
                            continue
                   k += 1
        else:
            continue
        all_images.append(all_data_for_SN)
                
        
#dump all_SN into supernovae
pickle.dump(all_images, open("all_images.pickle", 'wb'))

        
