Pycrawl
=======

A Web Spider/Indexer in Python for Hadoop
-----------------------------------------

####Quick and dirty setup instructions to be improved upon later: 
Requirements:
  * Hadoop
  * Hbase including running the thrift server


####HBase setup:
I've created both the tables inside the HBase shell via these commands:

create 'crawls', 'METADATA', 'PAGEDATA'
create 'anet', 'data'



####HDFS setup:
TBD
