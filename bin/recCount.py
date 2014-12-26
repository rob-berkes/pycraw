import psycopg2
conn = psycopg2.connect("dbname=words user=postgres")
cur  = conn.cursor()
cur.execute("SELECT * from crawls;")
print "Total words indexed: ",
print cur.rowcount
cur.execute("SELECT * FROM visits;")
print "Total pages indexed: ",
print cur.rowcount
print "Instances of: "
print "=============="
cur.execute("SELECT * from crawls WHERE word='the';")
print "the : ",
print cur.rowcount
cur.execute("SELECT * from crawls WHERE word='robert';")
print "robert : ",
print cur.rowcount
cur.execute("SELECT * from crawls WHERE word='obama';")
print "obama : ",
print cur.rowcount
cur.execute("SELECT * from crawls WHERE word='america';")
print "america : ",
print cur.rowcount
