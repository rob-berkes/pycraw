import wget 
import time
import urllib2
import socket
import psycopg2 
from bs4 import BeautifulSoup
from datetime import datetime
import re
MAXLOCALLINKCOUNT = 20
timeout = 5
socket.setdefaulttimeout(timeout)

exlink = re.compile(r'(http://)(.*)')
exslink = re.compile(r'(https://)(.*)')

ifp=open('54-149-p80.log','r')
class Word:
   url = ''
   word = ''
   position = 0

conn= psycopg2.connect("dbname=words user=postgres")
conn.autocommit = True
cur = conn.cursor()

def procAllLinks(soup,url):
  BASEURL = url
  ofile = open('newlinks.log','a')
  indexed = datetime.now()
  LINKCOUNT = 0
  for link in soup.find_all('a'):
    url = BASEURL
    try:
      if re.match(exlink,link.get('href')) or re.match(exslink,link.get('href')):
        try:
          ofile.write(link.get('href'))
          ofile.write('\n')
        except TypeError:
          pass
        except UnicodeDecodeError:
	  pass
        except UnicodeEncodeError:
	  pass
      else:
        LINKCOUNT+=1
        if LINKCOUNT > MAXLOCALLINKCOUNT:
          break
        try:
          url = BASEURL +str(link.get('href'))
        except UnicodeEncodeError:
          LINKCOUNT-=1
          pass
        req = urllib2.Request(url)
        html = ''
        try:
          html = urllib2.urlopen(req)
        except urllib2.HTTPError:
          pass
        except urllib2.URLError:
          pass
        full_text = soup.get_text()
        full_text = full_text.strip().split()
        COUNT=1
        print "-**************Indexing Local link: ",
        print url +" *************-"
        print html
        cur.execute("INSERT INTO visits (url, indexed) VALUES (%s, %s)", (url, indexed))
        for word in full_text:
          entry = Word()
          entry.word = word.lower()
          entry.position = COUNT
          entry.url = url
          cur.execute("INSERT INTO crawls (word, position, url) VALUES (%s, %s, %s)", (entry.word,entry.position,entry.url))
          COUNT+=1
    except TypeError:
      pass
  url = url
  req = urllib2.Request(url)
  try:
    html = urllib2.urlopen(req)
  except:
    pass
  full_text = soup.get_text()
  full_text = full_text.strip().split()
  COUNT=1
  for word in full_text:
    entry = Word()
    entry.word = word.lower()
    entry.position = COUNT
    entry.url = url
    cur.execute("INSERT INTO crawls (word, position, url) VALUES (%s, %s, %s)", (entry.word,entry.position,entry.url))
    COUNT+=1
  ofile.close() 

for line in ifp:
  line = line.strip().split()
#  hostn , aliasl, ipl = socket.gethostbyaddr(str(line[1]))
#  host = socket.getfqdn(hostn)
#  print host
#  quit()
  url = 'http://'+str(line[1])+'/'
  req = urllib2.Request(url)
  html = ''
  try:
    html = urllib2.urlopen(req)
  except urllib2.HTTPError:
    pass
  except urllib2.URLError:
    pass
  except:
    pass
  
  print "-======= site: "+str(line[1])+" =======-"
  print html
  print "now indexing ..."
  try:
    soup = BeautifulSoup(html)
  except TypeError:
    pass
  procAllLinks(soup,url)
 
#  try:
#    wget.download(url,out='html/'+str(line[1])+'index.html')
#  except IOError:
#    continue
