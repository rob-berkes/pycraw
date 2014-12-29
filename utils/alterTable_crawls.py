import psycopg2
conn=psycopg2.connect("dbname=words user=postgres")
cur = conn.cursor()
cur.execute("ALTER TABLE crawls ADD linkid serial4;")
conn.commit()
conn.close()
