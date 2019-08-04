# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:27:10 2019

@author: tickc
"""


filename = 'C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/male.txt'
filename1 = 'C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/female.txt'

with open(filename,'r') as document:
    usmaledict = {}
    for line in document:
        if line.strip():            
            key, value = line.split(None, 1)
            key = key.lower()
            usmaledict[key] = value.split()           
 
with open(filename1,'r') as document:
    usfemaledict = {}
    for line in document:
        if line.strip():            
            key, value = line.split(None, 1)
            key = key.lower()
            usfemaledict[key] = value.split()     
