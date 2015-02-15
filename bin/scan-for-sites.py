from pywebhdfs.webhdfs import PyWebHdfsClient
import happybase
import subprocess
import time
hdfs = PyWebHdfsClient(host='namenode',port='50070',user_name='root')
conn=happybase.Connection('127.0.0.1')
for  a_net in range(54,55):
  for bnet in range(0,256):
    IPADDR=str(a_net)+'.'+str(bnet)+'.0.0/16'
    OFILE=str(a_net)+'-'+str(bnet)+'-p80.log'
    A=subprocess.Popen(['masscan','-p80','-oG',OFILE,IPADDR,'--rate=2000'])
    A.wait()
    time.sleep(2)
    HADOOP_FILE_NAME='user/root/scans/'+str(a_net)+'/'+OFILE
    with open(OFILE) as ofp:
      hdfs.create_file(HADOOP_FILE_NAME,ofp)
    subprocess.Popen(['rm',OFILE])
