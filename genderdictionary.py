# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:03:40 2019

@author: tickc
"""


f = open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/nam_dict.txt')

genderDict = {}
shortNames = []
count = 0 

for line in f:
    if count >= 364:
        text = line[0:86]
        mf = text[:2].strip() # M,1M,?M, F,1F,?F, ?, =
        #  =  <short_name> <long_name> 
        name = text[2:29].lower().strip()
        sortingFlag = text[29] # +,-; ignore +
        frequencies = text[30:-2]

        if sortingFlag != '+':
                    if mf == '=':
                        shortNames.append([name, frequencies])
                    else:
                        if name.find('+') != -1:
                            names = [name.replace('+','-'), name.replace('+',' '), name.replace('+','').capitalize()]
                        else:
                            names = [name]
                        for name in names:
                            if name in genderDict:
                                genderDict[name].append([mf, frequencies])
                            else:
                                genderDict[name] = [[mf, frequencies]]
    count += 1
    
for [name, frequencies] in shortNames:
    shortName, longName = name.split()
    if shortName in genderDict and not longName in genderDict:
        for nameList in genderDict[shortName]:
            if longName in genderDict:
                genderDict[longName].append(nameList)
            else:
                genderDict[longName] = [nameList]
            
    elif longName in genderDict and not shortName in genderDict:
        for nameList in genderDict[longName]:
            if shortName in genderDict:
                genderDict[shortName].append(nameList)
            else:
                genderDict[shortName] = [nameList]
#    
#    #columns = line.split(' ') # ',' or '\t' or ' ' etc...