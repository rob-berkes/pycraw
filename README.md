Pycrawl
=======

A Web Spider/Indexer in Python for Hadoop
-----------------------------------------

####Quick and dirty setup instructions to be improved upon later: 
Requirements:
  * Hadoop
  * Hbase including running the thrift server
  * Robert David Graham's excellent masscan tool https://github.com/robertdavidgraham/masscan

Python pip libraries required:
  * happybase
  * pywebhdfs

####HBase setup:
I've created both the tables inside the HBase shell via these commands:

create 'crawls', 'METADATA', 'PAGEDATA'
create 'anet', 'data'
#create 'words', 'metadata'


####HDFS setup:
As root:

hadoop/bin/hdfs dfs -mkdir crawls/
hadoop/bin/hdfs dfs -mkdir scans/
hadoop/bin/hdfs dfs -mkdir texts/



