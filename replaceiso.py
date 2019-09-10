# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:44:11 2019

@author: tickc
"""

import fileinput

filename = open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/nam_dict.txt')

text_to_search = '<Ê>'
replacement_text = chr(282)

with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(text_to_search, replacement_text), end='')