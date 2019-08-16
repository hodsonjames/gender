import nltk
import random


#extracts features from labeled_names names 
def extract_features(name):
    name = name.lower()
    return {
        'last_char': name[-1],
        'last_two': name[-2:],
        'last_three': name[-3:],
        'first': name[0],
        'first2': name[:2]
    }

f_names = listmale
m_names = listfem

all_names = [(i, 'm') for i in m_names] + [(i, 'f') for i in f_names]
random.shuffle(all_names)

#splits feature sets into training and test sets
test_set = all_names[500:]
train_set= all_names[:500]

# The training set is used to train a new "naive Bayes" classifier. 
test_set_feat = [(extract_features(n), g) for n, g in test_set]
train_set_feat= [(extract_features(n), g) for n, g in train_set]

classifier = nltk.NaiveBayesClassifier.train(train_set_feat)
print(classifier.classify(extract_features('john'))) 
print(nltk.classify.accuracy(classifier, train_set_feat))

