import glob
from pymongo import Connection
from bs4 import BeautifulSoup
import psycopg2
import subprocess
import re
conn = psycopg2.connect("dbname=words user=postgres")
conn.autocommit=True
cur = conn.cursor()
class Word:
   url = ''
   word = ''
   position = 0
rx = re.compile(r'(html/)(.*)(index.html)')
for fn in glob.glob('html/*.html'):
    print "======== "+str(fn)+" ========="
    p = re.match(rx,fn)
    try:
      url = p.group(2)
    except AttributeError:
      pass 
    soup = BeautifulSoup(open(fn))
    full_text = soup.get_text()
    full_text = full_text.strip().split()
    COUNT=1
    for word in full_text:
      entry = Word()
      entry.word = word.lower()
      entry.position = COUNT
      entry.url = url
      print entry.word, entry.position, entry.url
      cur.execute("INSERT INTO crawls (word, position, url) VALUES (%s, %s, %s)", (entry.word,entry.position,entry.url))
      COUNT+=1
    print "moving file "+str(fn)+" to arc/ ..."
    subprocess.call(["mv",fn,"arc/"]) 
conn.commit()
conn.close()
