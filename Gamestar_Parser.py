import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import nltk
import time





def spieleListe():
    urllist = []
    fileid = 1096
    for seiten in range(74,103):
        urllist = []
        print "-_-_"*20
        print "Seite: ", seiten
        print "-_-_"*20
        url = "http://www.gamestar.de/index.cfm?pid=646&p="
        url = "%s%s" % (url, seiten)
        webpage =  urllib.urlopen(url).read()
        soup = BeautifulSoup(webpage)
        mydivs = soup.findAll("a", { "class" : "linkProductM teaserTextTitle" })
        
        
        for divs in mydivs:
            url =  (divs.get("href"))
            text = (divs.get_text())
            url = "%s%s" % ("http://www.gamestar.de", url)
            writingtofile(url, fileid)
            fileid += 1
            time.sleep(1)

    return urllist
  


contentlist = []
ratinglist = []

def reviewparser(url, deflist, ratings):
    webpage =  urllib.urlopen(url.encode("utf-8")).read()
    soup = BeautifulSoup(webpage)
    content = str(soup.findAll("p"))
    content = nltk.clean_html(content)
    content = content
    deflist.append(content)
    
    next = soup.findAll("div", { "class" : "pageright" })
    
    
    rating = soup.findAll("span", { "class" : "teaserRatingScore" })
    if rating >0:
        for i in rating:
            rating = i.get_text()
            print rating
            if int(rating) >0:
                ratings.append(rating)
            else:
                nothing = "nothing"
    
    if len(next)>0:
        for i in next:
            expression = re.compile("href=\"(.*)\"")
            string = str(i)
            urlendung =  re.findall(expression, string)
            url = "%s%s" % ("http://www.gamestar.de/", urlendung[0])
            next = 1
            reviewparser(url, deflist, ratings)
            
            
    else:
        nothing = "nothing"
    
    return deflist, ratings


def writingtofile(url, fileid):
    deflist = []
    ratings = []
    deflist, ratinglist = reviewparser(url, deflist, ratings)
    for i in range(0,len(ratinglist)):
        rating = ratinglist[i]
        content = " ".join(deflist)
        file = open("Textfiles/GS%s - Rating %s.txt" % (fileid, int(rating)), "w")
        file.write(content)
        file.close()
        print "File: ", fileid
        
        

spieleListe()

