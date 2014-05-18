import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import nltk
import time

totalStart = time.time()


#Review Seiten: 1 bis 355

def mainpage():
    fileid = 1147
    seite = 25
    for i in range(25,356):
        url_gen = "http://www.rogerebert.com/reviews/page/"
        url = "%s%s" % (url_gen, i)
        
        webpage = urllib.urlopen(url).read()
        soup = BeautifulSoup(webpage)
    
        mydivs = soup.findAll("figure", { "class" : "movie review" }) 
        
        
        print "Seite: ", seite
        seite += 1
        for text in mydivs:
            text = str(text)
            movieTitleComp = re.compile("<a href=\".*\">(.*)</a>")
            movieTitleFind = re.findall(movieTitleComp, text)
            
            urlComp = re.compile("<a href=\"(.*)\">.*</a>")
            urlFind = re.findall(urlComp, text)
            

            
            newurl = "%s%s" %("http://www.rogerebert.com", urlFind[0])
            reviewParser(newurl, fileid)
            fileid += 1
            
            
        
    
        

def reviewParser(url, fileid):
    reviewList = []
    ratingList = []
    
    
    webpage = urllib.urlopen(url).read()
    soup = BeautifulSoup(webpage)
    
    reviewBody = soup.findAll("div", {"itemprop": "reviewBody"})
    reviewRating = soup.findAll("span", {"itemprop": "reviewRating"})
    
    
    for text in reviewBody:
        reviewContent =  text.get_text()
        reviewList.append(reviewContent)
        
        
      
    for text in reviewRating:
        text = str(text)
        ratingComp = ("<meta content=\"(.*)\".* itemprop=\"ratingValue\"/>")
        
        #Filme ohne Rating haben keine 0.0 Sterne sondern ueberhaupt keine Sterne. Dementsprechend kann man mit regular expressions nichts finden
        if re.findall(ratingComp, text):
            ratingFind = re.findall(ratingComp, text)
            ratingList.append(ratingFind[0])
        else:
            ratingList.append(0.0)
    
    currentTime = time.time()
    print "Script running: ", currentTime -totalStart, " Seconds"
    print "Currently at File: ", fileid    
    print "-_-_"*40
    
    contentList = [reviewList, ratingList]
    writerFunc(contentList, fileid)
    
    time.sleep(1)    
    

def writerFunc(content, fileid):
    review, rating = content[0], content[1]
    review = review[0].encode('utf-8')
    rating = rating[0]
    
    filename = ("Textfiles/ID %s - Rating %s.txt")% (fileid, rating)
    file = open(filename, "w")
    file.write(review)
    file.close()
    
    








mainpage()

totalEnd = time.time()
totalTime = totalEnd - totalStart
print "entire processing time took: ", totalTime, " seconds"
print "######"*30