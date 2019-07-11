# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:45:42 2019

@author: tickc
"""

textname = input("nam_dict.txt")
thetextfile = open(textname,'r')
print("The file has been successfully opened!")
thetextfile = thetextfile.read()
file_s = thetextfile.split()
holder = []
wordlist = {}
for c in file_s:
   wordlist[c.split()[0]] = c.split()[1:]