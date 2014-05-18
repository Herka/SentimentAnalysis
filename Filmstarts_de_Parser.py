from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import nltk
import codecs
import time

fileid= 6938

seite = 343

for i in range(347,348):
    
    url = "%s%s" % ("http://www.filmstarts.de/kritiken/neuste-kritiken/?page=",i)
    

    webpage =  urllib2.urlopen(url).read()
    soup = BeautifulSoup(webpage)
    
    

    
    pettysoup = soup.prettify()
    
    mydivs = soup.findAll("div", { "class" : "rubric" })
    
    titel = soup.findAll("div", { "class" : "img_side_content" })
    titel2 = soup.findAll("a", { "class" : "no_underline" })
    
    unterseite = 1
    
    urllist = []
    for text in titel2:
        url =  (text.get("href"))
        urllist.append(url)
    
    
    for url in urllist:
        url= "%s%s%s" % ("http://www.filmstarts.de",url[:-5], "/kritik.html")
        try:
            webpage =  urllib2.urlopen(url).read()
            soup = BeautifulSoup(webpage)
            
            filmname = soup.findAll("span",{"class": "fs11 lighten"})
            for i in filmname:
                filmname= i.get_text().encode('utf-8')
            
            review = soup.findAll("div", {"class" : "margin_20b"})
        
            review = review[0]
            text= review.get_text().encode('utf-8')
            text = nltk.word_tokenize(text)
            rating = text[0]
            text = text[4:-1]
            text = nltk.Text(text)
            print len(text)
            print rating
            print "Seite: ",seite
            print "Review: ", unterseite
            unterseite += 1
    
            
            filename = ("Textfiles/ID %s - Rating %s.txt")% (fileid, rating)
            file = open(filename, "w")
            for words in text:
                file.write(words)
                file.write(" ")
            file.close()
            fileid += 1
            print "----Ende-----"
            #time.sleep(5)
        except:
            continue
    seite += 1
        
        
       
