import happybase
import pydoop.hdfs as hdfs
import os
from bs4 import BeautifulSoup

conn=happybase.Connection('127.0.0.1')
crawlTbl=conn.table('crawls')

ANET=125

for BNET in range(33,40):
  for CNET in range(0,255):
    for DNET in range(0,255):
      FNAME  =str(ANET)+"."+str(BNET)+"."+str(CNET)+"."+str(DNET)+"_root20150114.htm"
      GETFILE="crawls/"+str(ANET)+"/"+str(BNET)+"/"+FNAME
      print FNAME	
      try:
        hdfs.get(GETFILE,FNAME)
      except IOError:
	print BNET,CNET,DNET
	continue
      soup=BeautifulSoup(open(FNAME,'r'))
      for anchor in soup.find_all('a'):
	link = anchor.get('href')
      for key, data in table.rows([FNAME]):
	print key,data
	break





      FNAME.close()
      os.remove(FNAME)
	
