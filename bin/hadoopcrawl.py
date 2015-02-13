from pywebhdfs.webhdfs import PyWebHdfsClient
import time
import urllib2
import socket
from bs4 import BeautifulSoup
from datetime import datetime
import os
import happybase
import re
import pickle

client=PyWebHdfsClient(host='namenode',port='50070',user_name='root')
conn=happybase.Connection('127.0.0.1')
crawls=conn.table('crawls')
MAXLOCALLINKCOUNT = 30
timeout = 5
socket.setdefaulttimeout(timeout)
DATESTRING=str(time.strftime('%Y%m%d'))
ANET=60
for BNET in range(0,11):
  SCANSITESFILE=str(ANET)+'-'+str(BNET)+'-p80.log'
  FNAME='user/root/scans/'+str(ANET)+'/'+SCANSITESFILE
  SSFP=open(SCANSITESFILE,'w')
  SSFP.write(client.read_file(FNAME))
  SSFP.close()
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
    HADOOP_HTMLFILE='user/root/crawls/'+str(ANET)+'/'+str(BNET)+'/'+HTMLFILE
    HADOOP_TEXTFILE='user/root/texts/'+str(ANET)+'/'+str(BNET)+'/'+TEXTFILE
    print "-======= site: "+str(url)+" =======-"
    try:
      soup = BeautifulSoup(html)
    except:
      print " soup exception"
      continue
    HFP=open(HTMLFILE,'w')
    HFP.write(soup.encode('utf-8'))
    HFP.close()
    client.create_file(HADOOP_HTMLFILE,HTMLFILE)

    TFP=open(TEXTFILE,'w')
    WRITEOUT=unicode(soup.get_text())
    WORDLIST=re.sub(r'[^a-zA-Z0-9 ]',r' ',WRITEOUT)
    WORDLIST=WORDLIST.strip().split()
    TFP.write(WRITEOUT.encode('utf-8'))
    TFP.close()
    client.create_file(HADOOP_TEXTFILE,TEXTFILE)

    time.sleep(1)
    
    crawls.put(line[1],{'METADATA:ipaddr':line[1],'METADATA:htmlLocation':HADOOP_HTMLFILE,'METADATA:textLocation':HADOOP_TEXTFILE,'METADATA:scanLocation':FNAME,'PAGEDATA:wordlist':pickle.dumps(WORDLIST)})
    os.remove(HTMLFILE)
    os.remove(TEXTFILE)
  ifp.close()
  os.remove(SCANSITESFILE)
