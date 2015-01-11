from data2dict import data2dict
from bs4 import BeautifulSoup

def parse(localpage = None): #We can use local storage as an input, just provide the directory
    if localpage:
        f=open('page.htm','r') #if we want to use the local page, just pull it from the directory
        pgsrc=f.read()
        f.close()
        
    else:
        import urllib2
        url = 'https://secure.hosting.vt.edu/www.opel.ece.vt.edu/queue.php'
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'} 
        request = urllib2.Request(url, None, headers)

        response = urllib2.urlopen(request,None,5)
        
        pgsrc = response.read()
    
    soup=BeautifulSoup(pgsrc)
    bigqsrc = soup.find_all('table')[3].find_all('tr')
    bigqsrc=bigqsrc[1:] #cut out the table headers (they mess with the data)
    
    bigq=[]
    for person in bigqsrc:
        dlist=person.find_all('td') 
        bigq+=[data2dict(dlist)]

    return bigq
