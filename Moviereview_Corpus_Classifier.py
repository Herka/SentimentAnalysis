#based on: http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
#und: http://streamhacker.com/2010/10/25/training-binary-text-classifiers-nltk-trainer/

# -*- coding: utf-8 -*-
import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle
 

 
def word_feats(words):
    return dict([(word, True) for word in words])
 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'negative') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'positive') for f in posids]
 
negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
 
#Teilung um gleich testen zu koennen wie gut der Classifier funktioniert. 
#trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
#testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

#komplette Liste
trainfeats = negfeats + posfeats
#print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
 
classifier = NaiveBayesClassifier.train(trainfeats)


cl.show_most_informative_features(n=30)
