import wget 
import time
import urllib2
import socket
import psycopg2 
from bs4 import BeautifulSoup
timeout = 5
socket.setdefaulttimeout(timeout)

ifp=open('54-149-p80.log','r')
class Word:
   url = ''
   word = ''
   position = 0
conn= psycopg2.connect("dbname=words user=postgres")
cur = conn.cursor()
for line in ifp:
  line = line.strip().split()
  url = 'http://'+str(line[1])+'/'
  req = urllib2.Request(url)
  html = ''
  try:
    html = urllib2.urlopen(req)
  except urllib2.HTTPError:
    pass
  except urllib2.URLError:
    pass
  
  print "-======= site: "+str(line[1])+" =======-"
  print html
  print "now indexing ..."
  soup = BeautifulSoup(html)
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
 
#  try:
#    wget.download(url,out='html/'+str(line[1])+'index.html')
#  except IOError:
#    continue
