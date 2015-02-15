Pycrawl
=======

A Web Spider/Indexer in Python for Hadoop
-----------------------------------------

####Quick and dirty setup instructions to be improved upon later: 
Requirements:
  * Hadoop
  * Hbase including running the thrift server
  * Robert David Graham's excellent masscan tool https://github.com/robertdavidgraham/masscan

####HBase setup:
I've created both the tables inside the HBase shell via these commands:

create 'crawls', 'METADATA', 'PAGEDATA'
create 'anet', 'data'



####HDFS setup:
TBD


