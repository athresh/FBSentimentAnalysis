import nltk
import csv
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
import matplotlib.pyplot as plt
import numpy as np
from ggplot import *


stopset = list(set(stopwords.words('english')))

def word_feats(words):
    return dict([(word, True) for word in words.split() if word not in stopset])


with open('C:/Users/Athresh/Documents/ATH ML/Python/Sentiment analysis dataset.csv', 'r',encoding='UTF-8') as f:
    reader = csv.reader(f)
    data_as_list = list(reader)

del data_as_list[0]
del data_as_list[8750:8875]
count =0

random.Random(2).shuffle(data_as_list)

#Preprocessing
while count<len(data_as_list):
    data_as_list[count][3]=data_as_list[count][3].strip()
    data_as_list[count][3]=data_as_list[count][3].lower()
    del data_as_list[count][2]
    del data_as_list[count][0]
    data_as_list[count][1], data_as_list[count][0] = data_as_list[count][0], data_as_list[count][1]
    if data_as_list[count][1]=='0':
        data_as_list[count][1]='neg'
    elif data_as_list[count][1]=='1':
        data_as_list[count][1]='pos'

    data_as_list[count][0]=word_feats(data_as_list[count][0])
    count = count + 1

#Dividing the data into training and test sets
trainFeats = 1000000
testFeats = 100000
training=data_as_list[:trainFeats]
testing = data_as_list[trainFeats+100000:trainFeats+testFeats+100000]
classifier= NaiveBayesClassifier.train(training)
classifier.show_most_informative_features()

#Testing on data collected from facebook.
fp = 'C:/Users/Athresh/Documents/ATH ML/Python/FBfeedDataLabel.csv'
def calcAccuracyOnTestData(filepath,cl):
    negCount=0
    posCount=0
    with open(filepath, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        testdata_as_list = list(reader)
        for x in range(0, len(testdata_as_list)) :
            testdata_as_list[x][0] = word_feats(testdata_as_list[x][0])
            if cl.classify(testdata_as_list[x][0]) == 'neg':
                negCount = negCount + 1
            elif cl.classify(testdata_as_list[x][0]) == 'pos':
                posCount = posCount + 1
        accuracy = nltk.classify.util.accuracy(cl, testdata_as_list)
        print('Positive fb:', posCount)
        print('Negative fb:', negCount)
        print('Accuracy on fb data: ', round(nltk.classify.util.accuracy(cl, testdata_as_list),2))
        return accuracy , posCount, negCount

#Testing on the test set portion of the tweets data
negTwitter = 0
posTwitter = 0
testResults = calcAccuracyOnTestData(fp,classifier)
for x in range(0, len(testing)) :
    if classifier.classify(testing[x][0]) == 'neg':
        negTwitter = negTwitter + 1
    elif classifier.classify(testing[x][0]) == 'pos':
        posTwitter = posTwitter + 1

print('Negative twitter: ',negTwitter)
print('Positive twitter: ', posTwitter)
print('Accuracy on twitter test data: ', round(nltk.classify.util.accuracy(classifier, testing),2))

