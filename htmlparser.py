from bs4 import BeautifulSoup
import sys,urllib2, codecs



if __name__ == '__main__':
    url = "http://course-query.acad.ncku.edu.tw/qry/"
    type = sys.getfilesystemencoding()
    #content = urllib2.urlopen(url).read().decode('utf-8').encode(type)
    #print content
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content,from_encoding="utf8")
    print soup.encode('gb18030')
    
    ##soup = BeautifulSoup(content.read().prettify().encode('utf-8'))
    #print soup;
    pass