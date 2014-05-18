# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
import json
import re
import pickle
 
#******
#Baut auf folgendes Tut: http://www.sjwhitworth.com/sentiment-analysis-in-python-using-nltk/
#****** 
 
postxt = []
negtxt = []

def sentimentFunct():
    countdown = 0
    sentimentlist = []
    afinnfile = open("AFINN.txt")
    
    scores = {} # initialize an empty dictionary

    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.

    #
    with open("ESCTweets.txt") as f:
        x = 0
        
        for line in f:
            #print line
        
            if len(line) >= 100:
                x =+ 1
                sentiment = 0
                try:
                    tweetdict = json.loads(line)
    
                except ValueError:
                    # decoding failed
                    continue
            
                text = tweetdict["text"]
                #print text
                wordlist = text.split(" ")
                #.lower(), weil die AFINN und ANEW liste nur lowercase woerter beinhaltet. 
                for word in wordlist:
                    try:
                        if word.lower() in scores:
                            sentiment += scores[word]
                    except KeyError:
                        #hat nicht funktioniert, Windows hat probleme mit Tweets
                        continue
                        
                sentimentlist.append(sentiment)
                
                
                if sentiment >5:
                    postxt.append(tweetdict["text"])
                if sentiment <-5:
                    negtxt.append(tweetdict["text"])
                
    return (postxt, negtxt)


 

postxt, negtxt = sentimentFunct()




neglist = []
poslist = []
 
#Create a list of 'negatives' with the exact length of our negative tweet list.
for i in range(0,len(negtxt)):
    neglist.append('negative')
 
#Likewise for positive.
for i in range(0,len(postxt)):
    poslist.append('positive')



#Creates a list of tuples, with sentiment tagged.
postagged = zip(postxt, poslist)
negtagged = zip(negtxt, neglist)
 
 
#Combines all of the tagged tweets to one large list.
taggedtweets = postagged + negtagged

tweets = []


#Create a list of words in the tweet, within a tuple.
for (word, sentiment) in taggedtweets:
    #word_filter = [i.lower() for i in word.split()]
    word = word.lower()
    word_filter = nltk.word_tokenize(word)
    #print word_filter
    tweets.append((word_filter, sentiment))


#Pull out all of the words in a list of tagged tweets, formatted in tuples.
def getwords(tweets):
    allwords = []
    for (words, sentiment) in tweets:
        allwords.extend(words)
    return allwords

 
#Order a list of tweets by their frequency.
def getwordfeatures(listoftweets):
    #Print out wordfreq if you want to have a look at the individual counts of words.
    wordfreq = nltk.FreqDist(listoftweets)
    words = wordfreq.keys()
    word.decode("utf-8")
    return words

def stopwordfilter():
    #Baut auf die ersten Funktionen auf und Filtert die Wordlist durch mehrere unterschiedliche Wortfilter
    
    print "Woerter ohne Filter: ",len(getwordfeatures(getwords(tweets)))
    #Erste Filter nimmt Woerter aus der NLTK Stopword liste
    wordlist = [i for i in getwordfeatures(getwords(tweets)) if not i in stopwords.words('english')]
    print "Nach ersten Filter: ",len(wordlist)
    
    
    
    #zweiter Filter: multilanguae stopwordliste, aehnlich denen der aus NLTK aber Mehrsprachig. Insgesamt etwa 6000 Worte
    stopwordfile= open("MultilanguageStopwords.txt", "r")
    stopwordtext = stopwordfile.readlines()
    stopwordtext = ", ".join(stopwordtext)
    stopwordtext.decode("utf-8")
    tokenized = nltk.word_tokenize(stopwordtext)
    wordlist = [i for i in wordlist if not i in tokenized]
    print "Nach zweitem Filter: ",len(wordlist)
    
    
    
    
    #dritter Filter: Customwordlist und wortlaenge (kleiner als 4 zeichen)
    
    wordlist = [i for i in wordlist if not len(i) < 4]
            
    customstopwordlist = ["#esc", "#esc2013", "#eurovision", "rt", "#france", "singing", "singer", "people", ":)", ",", ".", ":", "http"]
    #sucht alle Twitternamen mithilfe von re. "0oderMehr -@- 0 oder mehr w�rter
    for i in wordlist:
        finder = re.search(r'@.*', i)
        if finder:
            finder = finder.group()
            customstopwordlist.append(finder)
        
    
    wordlist = [i for i in wordlist if not i in customstopwordlist]
    print "Nach dritten Filter: ",len(wordlist)
    return wordlist


#F�r den komplizierteren vierten Filter eine eigene Funktion.
#Der Filter tagged die Saetze mithilfe von NLTK und u.a. alle propernouns (Namen etc.), Datumangaben, Sonderzeichen usw werden rausgefiltert
def nltkparser_filter(postxt, negtxt):
    x =0
    alltweets = []
    nounlist = []
    #Damit die Wortliste aus der Ersten "Filterfunktion" aufgerufen wird.
    wordlist = stopwordfilter()
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
            
        
        #print nounlist

        
    wordlist = [i for i in wordlist if not i in nounlist]
    print "Nach dem Noun Filter: ", len(wordlist)
    return wordlist


wordlist = nltkparser_filter(postxt, negtxt)



def feature_extractor(doc):
    docwords = set(doc)
    features = {}

    for i in wordlist:
       features[i] = (i in docwords)
    return features




#Erstellt das trainings set in dem passenden Format.
training_set = nltk.classify.apply_features(feature_extractor, tweets)


classifier = nltk.DecisionTreeClassifier.train(training_set)



print classifier.show_most_informative_features(n=30)


#Das Pickle Modul hilft es die Classifier dauerhaft zu speichern und in anderen Python Scripts wieder aufzurufen.
f = open("Twitter_Decision_Tree_Classifier.pickle", "wb")
pickle.dump(classifier, f)
f.close()
