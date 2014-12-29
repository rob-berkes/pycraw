import psycopg2
import urllib2
from bs4 import BeautifulSoup
GOURL='http://king5.com'

conn = psycopg2.connect("dbname=words user=postgres")
cur = conn.cursor()
req = urllib2.Request(GOURL)
html = urllib2.urlopen(req)
full_text = BeautifulSoup(html)
cur.execute("insert into textlinks (url, fulltext) VALUES (%s,%s);",(GOURL,str(full_text)))
conn.commit() 
cur.execute("select linkid from textlinks where url = %s;",(str(GOURL),))
print cur.fetchone()[0]

