import time
import urllib2
import socket
import psycopg2 
from bs4 import BeautifulSoup
from datetime import datetime
from lib.words import IgnoredList
import re
import os
MAXLOCALLINKCOUNT = 30
timeout = 5
socket.setdefaulttimeout(timeout)

exlink = re.compile(r'(http://)(.*)')
exslink = re.compile(r'(https://)(.*)')
javascriptlink = re.compile(r'(javascript)(.*)')

class Word:
   url = ''
   word = ''
   position = 0
   linktextid = ''

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
      HR = link.get('href')
      print HR
      if not re.match(exlink,HR) and not \
	     re.match(exslink,HR) and not \
	     re.match(javascriptlink,HR):
        try:
          ofile.write(HR)
          ofile.write('\n')
        except :
          print 'output file write error'
          continue
        LINKCOUNT+=1
        if LINKCOUNT > MAXLOCALLINKCOUNT:
          break
        try:
          url = BASEURL +unicode(HR)
        except UnicodeEncodeError:
	  print 'e4 uee'
          LINKCOUNT-=1
          continue
        req = urllib2.Request(url)
        html = ''
        try:
    	  print url
          html = urllib2.urlopen(req)
        except:
	  print 'url open error e5 uHE'
          continue
        COUNT=1
	LINKID=0
        print "-**************Indexing Local link: ",
        print url +" *************-"
        print html
  	full_text = soup.get_text()
	cur.execute("INSERT INTO textlinks (url, fulltext) VALUES(%s, %s)",(unicode(url),unicode(full_text)))
        cur.execute("SELECT linkid FROM textlinks WHERE url = %s",(url,))
	LINKID=cur.fetchone()[0] 
	full_text = full_text.strip().split()
        cur.execute("INSERT INTO visits (url, indexed) VALUES (%s, %s)", (url, indexed))
        for word in full_text:
	  word = sanitize(word)
          entry = Word()
          entry.word = word.lower()
          entry.position = COUNT
          entry.url = url
    #	  print entry.word, '\t',entry.position,'\t', entry.url
	  if word.lower() not in IgnoredList:
            cur.execute("INSERT INTO crawls (word, position, url,linkid) VALUES (%s, %s, %s, %s)", (entry.word,entry.position,entry.url,LINKID))
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
    if word.lower() not in IgnoredList:
      cur.execute("INSERT INTO crawls (word, position, url) VALUES (%s, %s, %s)", (entry.word,entry.position,entry.url))
    COUNT+=1
  ofile.close() 




ANET=54
for BNET in range(65,70):
  FNAME='scans/'+str(ANET)+'-'+str(BNET)+'--p80.log'
  try:
    ifp=open(FNAME,'r')
  except:
    continue
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
ifp.close()
os.remove(FNAME)
