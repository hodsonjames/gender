
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
shortNames = []

listmale = []
listfem =[]

accuracylist = []
valuelist = []

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
                
                
#frequencyDict = {}
#for i in genderDict:   
#    for j in genderDict[i]:          
#        for k in genderDict[i][j]:            
#            freq = genderDict[i][j][k]
#            if freq in frequencyDict:
#                frequencyDict[freq] += 1
#            else:
#                frequencyDict[freq] = 1
#
#russianpop = 0
#for name in genderDict:
#    for gender in genderDict[name]:
#        if 'russia' in genderDict[name][gender]:
#            russianpop += genderDict[name][gender]['russia']
#print(russianpop)

#Sorts names for male and female with values 
                
for key in genderDict.keys():
        if 'M' in genderDict[key]:
            listmale.append(key) 
        else:
            if 'F' in genderDict[key]:
                listfem.append(key) 
                  
import nltk
import random

testname = 'Phillip'

#removes vowels for feature extraction
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


#extracts features from labeled_names names 
def extract_features(name):
    
    name = name.lower()
    return {
        'last_char': name[-1],
        #'last_two': name[-2:],
        'last_three': name[-3:],
        'first': name[0],
        #'first2': name[:2],
        'first3': name[:3],
        'no_vowels': remove_vowels(name),
        'only_vowels': only_vowels(name),
    }

all_names = [(i, 'm') for i in listmale] + [(i, 'f') for i in listfem]

#loop to generate data for classifier

#while val <= len(all_names) * 0.8:

num_error_f = []
num_error_m = []
    
for x in range(0, 10):
    val = 2000
    
    random.shuffle(all_names)
    
    #splits feature sets into training and test sets
    test_set = all_names[val:]
    train_set= all_names[:val]
    
    # The training set is used to train a new "naive Bayes" classifier. 
    test_set_feat = [(extract_features(n), g) for n, g in test_set]
    train_set_feat= [(extract_features(n), g) for n, g in train_set]
    
    classifier = nltk.NaiveBayesClassifier.train(train_set_feat)    
    accuracy = nltk.classify.accuracy(classifier, test_set_feat)
    
    accuracylist.append(accuracy)
    valuelist.append(len(train_set))
    
#   val += int(len(all_names) * 0.8 * 5/100) 
    #val += 100
    error_list = []
    error_f = []
    error_m = []
    
    for i in test_set:
         if classifier.classify(extract_features(i[0])) != i[1]:
             error_list.append(i)
       
    #Create list off female and male erros        
    for i in error_list:
        if i[1] == 'f': 
            error_f.append(i)
        else:
            error_m.append(i)
           
    num_error_f.append(len(error_f))
    num_error_m.append(len(error_m))
                      

import matplotlib.pyplot as plt

x = num_error_f
y = num_error_m

plt.xlim(0,max(x))
plt.ylim(0,max(y))

plt.scatter(x,y)
plt.show()

print(classifier.classify(extract_features(testname)))
print(error_list)
print(error_f)
print(len(error_m))
print(len(test_set))
print(len(error_list)/len(test_set))  
#print(frequencyDict[0])
#    
#    #columns = line.split(' ') # ',' or '\t' or ' ' etc...