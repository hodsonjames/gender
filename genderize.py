"""
Created on Tue Sep 10 14:07:15 2019
@author: tickc
"""


import csv
import os 
import nltk
import random
#############################################################################
#
# A necessary utility for accessing the data local to the installation.
#
#############################################################################

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)
get_data("filename")

#using .split() will give incorrect values since it does not split whitespace
def split(values): 
    return [char for char in values] 

def remove_vowels(s):
    vowels = "aeiouAEIOU"
    s_without_vowels = ""
    for letter in s:
        if letter not in vowels:
            s_without_vowels += letter
    return s_without_vowels

def only_vowels(s):
    vowels = "aeiouAEIOU"
    only_vowels = ""
    for letter in s:
        if letter in vowels:
            only_vowels += letter
    return only_vowels

def extract_features(name):
    
    name = name.lower()
    return {
        'last_char': name[-1],
        'last_two': name[-2:],
        'last_three': name[-3:],
        'first': name[0],
        'first2': name[:2],
        'first3': name[:3],
        'no_vowels': remove_vowels(name),
        'only_vowels': only_vowels(name),
    }


    
class genderizer:

    def __init__(self):
        with open(get_data("country_pop.csv")) as g:
            self.pop = dict(filter(None, csv.reader(g)))
        
        self.f = open(get_data("nam_dict.txt"))
        
        self.countries = u"""great_britain ireland usa italy malta portugal spain france
                           belgium luxembourg the_netherlands east_frisia germany austria
                           swiss iceland denmark norway sweden finland estonia latvia
                           lithuania poland czech_republic slovakia hungary romania
                           bulgaria bosniaand croatia kosovo macedonia montenegro serbia
                           slovenia albania greece russia belarus moldova ukraine armenia
                           azerbaijan georgia the_stans turkey arabia israel china india
                           japan korea vietnam other_countries
                         """.split()
        
        
        self.genderDict = {}
        self.shortNames = []
        
        self.listmale = []
        self.listfem =[]
        
        self.count = 0
        
        for line in self.f:
            if self.count >= 362:
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
                                    if name not in self.genderDict:
                                        self.genderDict[name] = {}
                                        self.genderDict[name][mf] = {}                                   
                                    else:  
                                        if mf not in self.genderDict[name]:
                                            self.genderDict[name][mf] = {} 
                                            
                                    for country,freq in zip(self.countries,frequencies):
                                        if freq != ' ':
                                            norm_freq = int((float(self.pop[country]) * 1000) * 0.02 * (2 ** (int(freq,16) - 10)))
                                            #norm_freq = int(((float(pop[country]))*1000) * (math.log(int(freq,16))))
                                            # print(int(float(pop[country]) * 1000)) 
                                            # print((math.log(int(freq,16),2)))
                                            
                                            self.genderDict[name][mf][country] = norm_freq
               
            self.count += 1
        
        for [name, frequencies] in self.shortNames:
            shortName, longName = name.split()
            if shortName in self.genderDict and not longName in self.genderDict:
                for nameList in self.genderDict[shortName]:
                    if longName in self.genderDict:
                        self.genderDict[longName].append(nameList)
                    else:
                        self.genderDict[longName] = [nameList]
                    
            elif longName in self.genderDict and not shortName in self.genderDict:
                for nameList in self.genderDict[longName]:
                    if shortName in self.genderDict:
                        self.genderDict[shortName].append(nameList)
                    else:
                        self.genderDict[shortName] = [nameList]
                    
        #Sorts names for male and female with values 
                        
        for key in self.genderDict.keys():
                if 'M' in self.genderDict[key]:
                    self.listmale.append(key) 
                else:
                    if 'F' in self.genderDict[key]:
                        self.listfem.append(key) 
                      
        self.all_names = [(i, 'm') for i in self.listmale] + [(i, 'f') for i in self.listfem]
    
    
    #loop to generate data for classifier
    
    #while val <= len(all_names) * 0.8:
    
        for x in range(0, 1):
            val = 2000
            
            random.shuffle(self.all_names)
            
            #splits feature sets into training and test sets
            test_set = self.all_names[val:]
            train_set= self.all_names[:val]
            
            # The training set is used to train a new "naive Bayes" classifier. 
            test_set_feat = [(extract_features(n), g) for n, g in test_set]
            train_set_feat= [(extract_features(n), g) for n, g in train_set]
            
            self.classifier = nltk.NaiveBayesClassifier.train(train_set_feat)    
            self.accuracy = nltk.classify.accuracy(self.classifier, test_set_feat)
        
    def genderize(self,name,location = None):
        for key in self.genderDict.keys():
            if name in self.genderDict.keys() and location in self.genderDict[name]:
                if 'M' in self.genderDict[key]:
                    return 'm'
                else:
                    return 'f'
            if name in self.genderDict.keys() and location not in self.genderDict[name]:
                if 'M' in self.genderDict[key]:
                    return 'm'
                else:
                    return 'f'
            if name not in self.genderDict.keys():
                return self.classifier.classify(extract_features(name))
             
