import time
import urllib2
import socket
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pydoop.hdfs as hdfs
import happybase
conn=happybase.Connection('127.0.0.1')
crawls=conn.table('crawls')
hdfs.mkdir('crawls/')
MAXLOCALLINKCOUNT = 30
timeout = 5
socket.setdefaulttimeout(timeout)
DATESTRING=str(time.strftime('%Y%m%d'))
ANET=125
hdfs.mkdir('crawls/'+str(ANET)+'/')
hdfs.mkdir('texts/'+str(ANET)+'/')
for BNET in range(80,90):
  hdfs.mkdir('crawls/'+str(ANET)+'/'+str(BNET)+'/')
  hdfs.mkdir('texts/'+str(ANET)+'/'+str(BNET)+'/')
  SCANSITESFILE=str(ANET)+'-'+str(BNET)+'-p80.log'
  FNAME='scans/'+str(ANET)+'/'+SCANSITESFILE
  hdfs.get(FNAME,SCANSITESFILE)
  try:
   ifp=open(SCANSITESFILE,'r')
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
      print ' url open exception on '+str(url)
      continue
    soup=''
    HTMLFILE=str(line[1])+'_root'+DATESTRING+'.htm'
    TEXTFILE=str(line[1])+'_roottext_'+DATESTRING
    HADOOP_HTMLFILE='crawls/'+str(ANET)+'/'+str(BNET)+'/'+HTMLFILE
    HADOOP_TEXTFILE='texts/'+str(ANET)+'/'+str(BNET)+'/'+TEXTFILE
    print "-======= site: "+str(url)+" =======-"
    try:
      soup = BeautifulSoup(html)
    except:
      print " soup exception"
      continue
    HFP=open(HTMLFILE,'w')
    HFP.write(soup.encode('utf-8'))
    HFP.close()
    TFP=open(TEXTFILE,'w')
    WRITEOUT=unicode(soup.get_text())
    TFP.write(WRITEOUT.encode('utf-8'))
    TFP.close()
    time.sleep(1)
    
    try:
      hdfs.put(HTMLFILE,HADOOP_HTMLFILE)
    except IOError:
      print 'IOError on '+str(url)
      os.remove(HTMLFILE)
      os.remove(TEXTFILE)
      continue
    try:  
      hdfs.put(TEXTFILE,HADOOP_TEXTFILE)
    except IOError:
      print 'IOError on '+str(url)
      os.remove(HTMLFILE)
      os.remove(TEXTFILE)
      continue
    crawls.put(HTMLFILE,{'METADATA:ipaddr':line[1],'METADATA:htmlLocation':HADOOP_HTMLFILE,'METADATA:textLocation':HADOOP_TEXTFILE})
    os.remove(HTMLFILE)
    os.remove(TEXTFILE)
  ifp.close()
  os.remove(SCANSITESFILE)
