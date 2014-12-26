import psycopg2
conn=psycopg2.connection("dbname=words user=postgres")
cur = conn.cursor()
cur.execute("CREATE TABLE textlinks ( linkid serial4, url text, fulltext text, PRIMARY KEY(linkid) );")
conn.commit()
conn.close()
