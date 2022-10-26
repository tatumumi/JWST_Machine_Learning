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
has_sup = []
filt = ["F115W","F150W","F277W","F444W"]

#method to check if supernova places 16 pixels within border
def check_bound(i, j):
    if i >= 16 and i <= length - 16 and j >= 16 and j <= length -16:
        bound = 1
    else: 
        bound = 0
    return bound
    
 #method to crop image into 32 x 32   
def crop32(all_data_for_SN):
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
            
all_f115w_images = glob.glob("file-home-*F115W*_scale.fits")
all_f150w_images = glob.glob("file-home-*F150W*_scale.fits")
all_f277w_images = glob.glob("file-home-*F277W*_scale.fits")
all_f444w_images = glob.glob("file-home-*F444W*_scale.fits")
                             
for image in tqdm.tqdm(all_f115w_images):
    if all_f115w_imgages.count(image):
        check115 = True
    else:
        check115 = False
                             
    if all_f150w_images.count(image.replace('F115W', 'F150W')):
        check150 = True
    else:
        check150 = False
      
    if all_f277w_images.count(image.replace('F115W', 'F277W')):
        check277 = True
    else:
        check277 = False      
                                            
    if all_f444w_images.count(image.replace('F115W', 'F444W')):
        check444 = True
    else:
        check444 = False                                        
        
    if check115 & check150 & check277 & check444 == True:
        #for exists(image.replace(filt,"f150w"))
        print("all checks")
        all_data_for_SN = []
        k = 0
        while k < len(filt):
               print(k)
               img_name = image.replace("F115W", filt[k])
               print(img_name)
               h = fits.open(img_name)
               print(img_name)
               k += 1
               data = h[0].data
               length = len(data)
               header = h[0].header
               bound = 0
               i = h[0].header["SN_I"]
               j = h[0].header["SN_J"]
               #check if supernova was planted
               if h[0].header["PLACED"] == 'yes':
                  supernova = 1
                #adds image with nova into array
               else:
                      supernova = 0
                        #add filter adjustments for crop
               bound = check_bound(i,j)
               if bound == 1: 
                    all_data_for_SN = crop32(all_data_for_SN) 
               else:
                    continue
               h.close()
                
        if bound == 1:
            all_images.append(all_data_for_SN)
            has_sup.append(supernova)      
        
#dump all_SN into supernovae
pickle.dump((all_images, has_sup),open("all_images.pickle", 'wb'))
        
