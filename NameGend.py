import random 
from nltk.corpus import names 
import nltk 
  
#network uses just the last letter for prediction
#def gender_features(word): 
#    return {'last_letter':word[-1]} 

#Suffixes
#def gender_features(word):
#return {'suffix1': word[-1:],'suffix2': word[-2:]}

#First and last letter of name
def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features
   
labeled_names = ([(name, 'male') for name in names.words('male.txt')]+
             [(name, 'female') for name in names.words('female.txt')]) 

#array is in alphabetical order from the txt documents,  
#so I shuffled them for a proper random distribution 
random.shuffle(labeled_names) 
   
#extracts features from labeled_names names 
featuresets = [(gender_features2(n), gender)  
               for (n, gender)in labeled_names] 

#splits feature sets into training and test sets
train_set, test_set = featuresets[500:], featuresets[:500] 
  
# The training set is used to train a new "naive Bayes" classifier. 
classifier = nltk.NaiveBayesClassifier.train(train_set) 
  
print(classifier.classify(gender_features2('John'))) 
  
# output should be 'Male' 
# num value is classifier accuracy of train_set
print(nltk.classify.accuracy(classifier, train_set)) 
  
#classifier.show_most_informative_features(10)