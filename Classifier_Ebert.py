# -*- coding: utf-8 -*-
import os
import re
import nltk
import time
from nltk.corpus import stopwords
import pickle

startTime = time.time()

ebertFolder = os.listdir("C:\Users\Janis\Dropbox\Programmieren\Projects\NLTK_Classifier\Ebert_Reviews")

ebertNegList = []
ebertPosList = []

postxt = []
negtxt = []
print "Postxt laenge: ", len(postxt)
print "Negtxt laenge: ", len(negtxt)
def textfiles():
    fsratingcompiler = re.compile(".*Rating (.),")
    fsratingcompiler2 = re.compile(".*Rating.*,(.).txt")
    
    ebRatingComp = re.compile(".*Rating (...).txt")
    
    for file in ebertFolder:
        finder = re.findall(ebRatingComp, file)
        digit = float(finder[0])

        if digit > 3.0:
            ebertPosList.append(file)
        elif digit < 2.0:
            ebertNegList.append(file)
        
 
    return ebertPosList, ebertNegList

posEbert, negEbert = textfiles()       



def contentCollect(posEbert, negEbert):
    for i in posEbert:
        file = open("Ebert_Reviews/%s" % i, "r")
        content = file.read()
        content = content.lower()
        postxt.append(content)
        file.close()
        
    for i in negEbert:
        file = open("Ebert_Reviews/%s" % i, "r")
        content = file.read()
        content = content.lower()
        negtxt.append(content)
        file.close()
      

        



contentCollect(posEbert, negEbert)


def getWords():
    textcontent = []
    poslist = []
    neglist = []
    allwords = []
    for i in range(0, len(postxt)):
        poslist.append("positive")
    for i in range(0, len(negtxt)):
        neglist.append("negative")   
    #creates a list tuples with sentimenttxt tagged with positive or negative marking
    postagged = zip(postxt,poslist)
    negtagged = zip(negtxt, neglist)
    
    taggedcontent = postagged + negtagged

    #Create a list of words in the tweet, within a tuple.
    for (word, sentiment) in taggedcontent:
        #alt, ignoriert woerter mit kommat am ende: "haus,"
        #word_filter = [i.lower() for i in word.split()]
        #dauert deutlich laenger! ist aber besser
        word_filter = nltk.word_tokenize(word)

        for i in range(0,len(word_filter)):
            word_filter[i] = word_filter[i]
        textcontent.append((word_filter, sentiment))
        
    for (words, sentiment) in textcontent:
        allwords.extend(words)
    
       
    return textcontent, allwords


textcontent, allwords = getWords()  

def getwordfeatures(allwords):
    #sortiert woerter in absteigender haeufigkeit in der sie auftauchen
    #Print out wordfreq if you want to have a look at the individual counts of words.
    wordfreq = nltk.FreqDist(allwords)
    words = wordfreq.keys()
    return words

words = getwordfeatures(allwords)




def stopwordfilter(allwords):
     #Baut auf die ersten Funktionen auf und Filtert die Wordlist durch mehrere unterschiedliche Wortfilter
    
    print "Woerter ohne Filter: ",len(allwords)
    #Erste Filter nimmt Woerter aus der NLTK Stopword liste
    wordlist = [i for i in allwords if not i in stopwords.words('english')]
    print "Nach ersten Filter: ",len(wordlist)
    
    
    
    #zweiter Filter: multilanguae stopwordliste, aehnlich denen der aus NLTK aber Mehrsprachig. Insgesamt etwa 6000 Worte
    stopwordfile= open("MultilanguageStopwords.txt", "r")
    stopwordtext = stopwordfile.readlines()
    stopwordtext = ", ".join(stopwordtext)
    stopwordtext.decode("utf-8")
    tokenized = nltk.word_tokenize(stopwordtext)
    wordlist = [i for i in wordlist if not i in tokenized]
    print "Nach zweitem Filter: ",len(wordlist)
    
    
    #dritter Filter: Customwordlist
    customstopwordlist = ["time", "camera", "film", "films", "movie", "movies", "time", "singing", "singer", "people", ":)", ",", ".", ":"]
    #sucht alle Twitternamen mithilfe von re. "0oderMehr -@- 0 oder mehr w�rter
    for i in wordlist:
        finder = re.search(r'@.*', i)
        if finder:
            finder = finder.group()
            customstopwordlist.append(finder)
        
    
    wordlist = [i for i in wordlist if not i in customstopwordlist]
    print "Nach dritten Filter: ",len(wordlist)
    return wordlist






#Für den komplizierteren vierten Filter eine eigene Funktion.
#Der Filter tagged die Saetze mithilfe von NLTK und u.a. alle propernouns (Namen etc.), Datumangaben, Sonderzeichen usw werden rausgefiltert
def nltkparser_filter(postxt, negtxt):
    x =0
    alltweets = []
    nounlist = []
    #Damit die Wortliste aus der Ersten "Filterfunktion" aufgerufen wird.
    wordlist = stopwordfilter(allwords)
    for files in postxt, negtxt:
        for tweet in files:
            alltweets.append(tweet)
    for tweet in alltweets:
       
        
        tokenized = nltk.word_tokenize(tweet)
        tagged = nltk.pos_tag(tokenized)
        #finded NNP Nouns, andere zeichen
        nltklist = ["NNP", "CD", ",","(",")","\"", "''", "LS", "NNPS", "PRP", "PRP$", "SYM", "WDT", "WP", "WRB", "`", ":", "--", ".", "-" ]
        propernouns = [word.lower() for word,pos in tagged if pos in nltklist]
        for noun in propernouns:
            nounlist.append(noun)
            

    wordlist = [i for i in wordlist if not i in nounlist]
    print "Nach dem Noun Filter: ", len(wordlist)
    return wordlist




wordlist = nltkparser_filter(postxt, negtxt)
def feature_extractor(doc):
    docwords = set(doc)
    features = {}

    for i in wordlist:
       features[i] = (i in docwords))
    return features

 
#Creates a training set - classifier learns distribution of true/falses in the input.
training_set = nltk.classify.apply_features(feature_extractor, textcontent)



classifier = nltk.NaiveBayesClassifier.train(training_set)


print classifier.show_most_informative_features(n=100)




#Das Pickle Modul hilft es die Classifier dauerhaft zu speichern und in anderen Python Scripts wieder aufzurufen.
f = open("Ebert_Classifier.pickle", "wb")
pickle.dump(classifier, f)
f.close()



endTime = time.time()
print "Der Prozess hat: ", (endTime-startTime), " Sekunden gedauert."

