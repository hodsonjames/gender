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

#removes vowels from features
def remove_vowels(s):
    vowels = "aeiouAEIOU"
    s_without_vowels = ""
    for letter in s:
        if letter not in vowels:
            s_without_vowels += letter
    return s_without_vowels

#removes consonants from features
def only_vowels(s):
    vowels = "aeiouAEIOU"
    only_vowels = ""
    for letter in s:
        if letter in vowels:
            only_vowels += letter
    return only_vowels

#extracts features from name 
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
            
class Genderizer:

    def __init__(self):
        self.genderDict = {}
        self.listmale = []
        self.listfem = []
        
        self.buildDict()
        self.trainClassifier()
        
#Initializes dictionary for names                
    def buildDict(self):
        genderDict = {}
        shortNames = []
        listmale = []
        listfem =[]  
        Count = 0          
        #Acceses country_pop to get current population estimates for the population of each country
        pop = dict(filter(None, csv.reader(open(get_data("country_pop.csv")))))
        f = open(get_data("nam_dict.txt"))        
        #List of countries from 
        countries = u"""great_britain ireland usa italy malta portugal spain france
                           belgium luxembourg the_netherlands east_frisia germany austria
                           swiss iceland denmark norway sweden finland estonia latvia
                           lithuania poland czech_republic slovakia hungary romania
                           bulgaria bosniaand croatia kosovo macedonia montenegro serbia
                           slovenia albania greece russia belarus moldova ukraine armenia
                           azerbaijan georgia the_stans turkey arabia israel china india
                           japan korea vietnam other_countries
                         """.split()
               
        for line in f:
            if Count >= 362:
                #DOCUMENTATION_LENGTH = 362
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
                                            norm_freq = int((float(pop[country]) * 1000) * 0.02 * (2 ** (int(freq,16) - 10)))
                                            #norm_freq = int(((float(pop[country]))*1000) * (math.log(int(freq,16))))
                                            # print(int(float(pop[country]) * 1000)) 
                                            # print((math.log(int(freq,16),2)))
                                            
                                            genderDict[name][mf][country] = norm_freq
               
            Count += 1

        
        for [name, frequencies] in shortNames:
            shortName, longName = name.lower().split()
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
                    
        #Sorts names for male and female with values 
                        
        for key in genderDict.keys():
                if 'M' in genderDict[key]:
                    listmale.append(key) 
                else:
                    if 'F' in genderDict[key]:
                        listfem.append(key) 
#loop to generate data for classifier   
#while val <= len(all_names) * 0.8:
        self.genderDict = genderDict
        self.listmale = listmale
        self.listfem = listfem

    #Trains classifer for NLTK       
    def trainClassifier(self):
            all_names = [(i, 'm') for i in self.listmale] + [(i, 'f') for i in self.listfem]
            for x in range(0, 1):
                Val = 2000
                #DOCUMENTATION_LENGTH = 2000
                random.shuffle(all_names)
                
                #splits feature sets into training and test sets
                test_set = all_names[Val:]
                train_set= all_names[:Val]
                
                # The training set is used to train a new "naive Bayes" classifier. 
                test_set_feat = [(extract_features(n), g) for n, g in test_set]
                train_set_feat= [(extract_features(n), g) for n, g in train_set]
                
                self.classifier = nltk.NaiveBayesClassifier.train(train_set_feat)    
                self.accuracy = nltk.classify.accuracy(self.classifier, test_set_feat)           

    
    def genderize(self,name,location = None):
        name = name.lower()
        for key in self.genderDict.keys():
#            if name in self.genderDict.keys() and location != None:
#                if location in self.genderDict[name].keys():
#                    if 'M' in self.genderDict[key]:        
#                        return 'm'
#                    else:
#                        return 'f'
#                    
#                else:
#                    print(self.genderDict[name])
#                    return 'location not found'
                
            if name in self.genderDict.keys():
                print(name)
                if 'M' in self.genderDict[key]:
                    print(self.genderDict[key])
                    return 'm'
                else:
                    return 'f'

            if name not in self.genderDict.keys():
                print('classified')
                return self.classifier.classify(extract_features(name))
             
