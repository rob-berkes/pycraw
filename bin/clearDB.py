import psycopg2
import re

yes = re.compile(r'[Yy]')
conn = psycopg2.connect("dbname=words user=postgres")
cur = conn.cursor()

verify = raw_input("Are you sure (y/N)?")
if re.match(yes,verify):
  cur.execute('DELETE FROM crawls;')
  conn.commit()
  cur.execute('DELETE FROM visits;')
  conn.commit()
 

conn.close()
