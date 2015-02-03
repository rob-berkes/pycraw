from pyspark import SparkContext
ctx = SparkContext('spark://127.0.0.1/','SparkCount')

wordcounts = ctx.textFile('hdfs://127.0.0.1:54310/user/root/texts/') \
	.map(lambda x: x.replace(',','').replace(';','').replace('"','').replace('\'','').replace('.','').lower()) \
	.flatMap(lambda x: x.split()) \
	.map(lambda x: (x,1)) \
	.reduceByKey(lambda x,y:x+y) \
	.map(lambda x: (x[1],x[0])) \
	.sortByKey(False)

print wordcounts.take(10)
