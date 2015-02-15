from pywebhdfs.webhdfs import PyWebHdfsClient
import happybase
import subprocess
import time
from random import randint
HBASE_NODE='data2'
hdfs = PyWebHdfsClient(host='namenode',port='50070',user_name='root')
conn=happybase.Connection(HBASE_NODE)
t=conn.table('anet')
while True:
  a_net=randint(1,255)
  ROW=t.row(str(a_net))
  if len(ROW) > 0:
    for key, value in ROW.items():
        if value != str(-1):
          START=randint(1,255)
	  continue
  t.put(str(a_net),{'data:user':'thisnode'})
  print 'scanning the major '+str(a_net)+'.0.0.0/8 subnet'
  for bnet in range(0,256):
    if a_net==10:
       continue
    elif a_net==192 and bnet==168:
       continue
    elif a_net==172 and bnet==16:
       continue
    elif a_net==127:
       continue
    IPADDR=str(a_net)+'.'+str(bnet)+'.0.0/16'
    OFILE=str(a_net)+'-'+str(bnet)+'-p80.log'
    A=subprocess.Popen(['masscan','-p80','-oG',OFILE,IPADDR,'--rate=2000'])
    A.wait()
    time.sleep(2)
    HADOOP_FILE_NAME='user/root/scans/'+str(a_net)+'/'+OFILE
    with open(OFILE) as ofp:
      hdfs.create_file(HADOOP_FILE_NAME,ofp)
    subprocess.Popen(['rm',OFILE])
  t.put(str(a_net),{'data:user':'-1'})
