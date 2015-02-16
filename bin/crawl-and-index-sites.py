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
THRIFTNODE='data2'
client=PyWebHdfsClient(host='namenode',port='50070',user_name='root')
conn=happybase.Connection(THRIFTNODE) 
crawls=conn.table('crawls')
MAXLOCALLINKCOUNT = 30
timeout = 5
socket.setdefaulttimeout(timeout)
DATESTRING=str(time.strftime('%Y%m%d'))
ANET=187
for BNET in range(5,10):
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
    HTMLFILE=str(line[1])+'.htm'
    TEXTFILE=str(line[1])+'.txt'
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
    with open(HTMLFILE) as hfp:
      try:
        client.create_file(HADOOP_HTMLFILE,hfp)
      except:
        client.delete_file_dir(HADOOP_HTMLFILE)
        client.create_file(HADOOP_HTMLFILE,hfp)

    TFP=open(TEXTFILE,'w')
    WRITEOUT=unicode(soup.get_text())
    WORDLIST=re.sub(r'[^a-zA-Z0-9 ]',r' ',WRITEOUT)
    WORDLIST=WORDLIST.strip().split()
    TFP.write(WRITEOUT.encode('utf-8'))
    TFP.close()
    PAGETITLE=''
    try:
      PAGETITLE=soup.title.string
    except:
      pass
    try:
      PAGETITLE=PAGETITLE.encode('utf-8')
    except:
      pass
    try:
      PAGETITLE=unicode(PAGETITLE)
    except:
      pass
    HOSTPAGE=''
    try:
      HOSTPAGE,b,c=socket.gethostbyaddr(line[1])
    except:
      pass
    try:
      HOSTPAGE=HOSTPAGE.encode('utf-8')
    except:
      pass
    try:
      HOSTPAGE=unicode(HOSTPAGE)
    except:
      pass
   # position=0
   # for word in WORDLIST:
   #   position+=1
   #   words.put(line[1],{'metadata:word':word,'metadata:pagetitle':PAGETITLE,'metadata:position':position})
    with open(TEXTFILE) as tfp:
        try:
	  client.create_file(HADOOP_TEXTFILE,tfp)
        except:
	  client.delete_file_dir(HADOOP_TEXTFILE)
	  client.create_file(HADOOP_TEXTFILE,tfp)
    time.sleep(1)
    
    crawls.put(line[1],{'METADATA:daterun':DATESTRING,'METADATA:ipaddr':line[1],'METADATA:domain':HOSTPAGE,'METADATA:htmlLocation':HADOOP_HTMLFILE,'METADATA:textLocation':HADOOP_TEXTFILE,'METADATA:scanLocation':FNAME,'METADATA:numberOfWords':str(len(WORDLIST)),'PAGEDATA:wordlist':pickle.dumps(WORDLIST),'PAGEDATA:pagetitle':PAGETITLE})
    os.remove(HTMLFILE)
    os.remove(TEXTFILE)
  ifp.close()
  os.remove(SCANSITESFILE)
