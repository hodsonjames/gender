

import csv
with open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/country_pop.csv') as g:
    pop = dict(filter(None, csv.reader(g)))
    
f = open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/nam_dict.txt')

g = open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/male.txt','r')
h = open('C:/Users/tickc/OneDrive/Documents/GitHub/gender/data/female.txt','r')

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
usdict = {}
usfemaledict = {}
shortNames = []
count = 0 


with g as document:    
    for line in document:
        if line.strip():            
            key, value = line.split(None, 1)
            key = key.lower()
            usdict[key] = value.split()           
 
with h as document:    
    for line in document:
        if line.strip():            
            key, value = line.split(None, 1)
            key = key.lower()
            usfemaledict[key] = value.split()    

usdict.update(usfemaledict)      

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
                        continue
                    else:
                        if name.find('+') != -1:
                            names = [name.replace('+','-'), name.replace('+',' '), name.replace('+','').capitalize()]
                        else:
                            names = [name]
                        for name in names:
                            if name not in genderDict:
                                genderDict[name] = {}
                                genderDict[name][mf] = {}                                   
                            else:  
                                if mf not in genderDict[name]:
                                    genderDict[name][mf] = {} 
                                    
                            for country,freq in zip(countries,frequencies):
                                if freq != ' ':
                                    norm_freq = int((float(pop[country]) * 1000) * (2 ** (int(freq,16) - 10)))
                                    #norm_freq = int(((float(pop[country]))*1000) * (math.log(int(freq,16))))
                                    # print(int(float(pop[country]) * 1000)) 
                                    # print((math.log(int(freq,16),2)))
                                    
                                    genderDict[name][mf][country] = norm_freq
       
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
                
                
frequencyDict = {}
for i in genderDict:   
    for j in genderDict[i]:          
        for k in genderDict[i][j]:            
            freq = genderDict[i][j][k]
            if freq in frequencyDict:
                frequencyDict[freq] += 1
            else:
                frequencyDict[freq] = 1

#print(frequencyDict[0])
#    
#    #columns = line.split(' ') # ',' or '\t' or ' ' etc...