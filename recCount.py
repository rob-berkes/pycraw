import psycopg2
conn = psycopg2.connect("dbname=words user=postgres")
cur  = conn.cursor()
print cur.execute("SELECT count(*) from crawls;")
