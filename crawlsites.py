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

ifp=open('54-148-p80.log','r')
class Word:
   url = ''
   word = ''
   position = 0

conn= psycopg2.connect("dbname=words user=postgres")
conn.autocommit = True
cur = conn.cursor()

def sanitize (word):
  word = word.strip('#')
  word = word.strip(',')
  word = word.strip('.')
  word = word.strip('!')
  word = word.strip('?')
  word = word.strip(';')
  
  return word

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
        except :
          print 'output file write error'
          continue
        LINKCOUNT+=1
        if LINKCOUNT > MAXLOCALLINKCOUNT:
          break
        try:
          url = BASEURL +str(link.get('href'))
        except UnicodeEncodeError:
	  print 'e4 uee'
          LINKCOUNT-=1
          continue
        req = urllib2.Request(url)
        html = ''
        try:
          html = urllib2.urlopen(req)
        except:
	  print 'url open error e5 uHE'
          continue
        full_text = soup.get_text()
        full_text = full_text.strip().split()
        COUNT=1
        print "-**************Indexing Local link: ",
        print url +" *************-"
        print html
        cur.execute("INSERT INTO visits (url, indexed) VALUES (%s, %s)", (url, indexed))
        for word in full_text:
	  word = sanitize(word)
          entry = Word()
          entry.word = word.lower()
          entry.position = COUNT
          entry.url = url
    #	  print entry.word, '\t',entry.position,'\t', entry.url
          cur.execute("INSERT INTO crawls (word, position, url) VALUES (%s, %s, %s)", (entry.word,entry.position,entry.url))
          COUNT+=1
    except TypeError:
      print 'e7 TE'
      continue
  url = BASEURL
  req = urllib2.Request(url)
  try:
    html = urllib2.urlopen(req)
  except:
    print 'e8 generic'
  full_text = soup.get_text()
  full_text = full_text.strip().split()
  COUNT=1
  cur.execute("INSERT INTO visits (url, indexed) VALUES (%s, %s)", (url, indexed))
  for word in full_text:
    entry = Word()
    entry.word = word.lower()
    entry.position = COUNT
    entry.url = url
   # print entry.word, '\t',entry.position,'\t', entry.url
    cur.execute("INSERT INTO crawls (word, position, url) VALUES (%s, %s, %s)", (entry.word,entry.position,entry.url))
    COUNT+=1
  ofile.close() 

for line in ifp:
  line = line.strip().split()
  url = 'http://'+str(line[1])+'/'
  req = urllib2.Request(url)
  html = ''
  try:
    html = urllib2.urlopen(req)
  except:
    print ' url open exception'
    continue
  soup='' 
  print "-======= site: "+str(line[1])+" =======-"
  print html
  print "now indexing ..."
  try:
    soup = BeautifulSoup(html)
  except:
    print " soup exception"
    continue
  procAllLinks(soup,url)
