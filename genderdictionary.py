# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:03:40 2019

@author: tickc
"""


f = open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/nam_dict.txt')

countries = u"""great_britain ireland usa italy malta portugal spain france
                   belgium luxembourg the_netherlands east_frisia germany austria
                   swiss iceland denmark norway sweden finland estonia latvia
                   lithuania poland czech_republic slovakia hungary romania
                   bulgaria bosniaand croatia kosovo macedonia montenegro serbia
                   slovenia albania greece russia belarus moldova ukraine armenia
                   azerbaijan georgia the_stans turkey arabia israel china india
                   japan korea vietnam other_countries
                 """.split()

genderDict = {}
shortNames = []
count = 0 

def split(values): 
    return [char for char in values] 
#using .split() will give incorrect values since it does not split whitespace
    
for line in f:
    if count >= 362:
        text = line[0:86]
        mf = text[:2].strip() # M,1M,?M, F,1F,?F, ?, =
        #  =  <short_name> <long_name> 
        name = text[2:29].lower().strip()
        sortingFlag = text[29] # +,-; ignore +
        unsortedf = text[30:85]
        frequencies = split(unsortedf)
    
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