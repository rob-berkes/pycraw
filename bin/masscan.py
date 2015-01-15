import subprocess
import pydoop.hdfs as hdfs
import time
for  a_net in range(124,133):
  hdfs.mkdir('scans/'+str(a_net))
  for bnet in range(0,256):
    IPADDR=str(a_net)+'.'+str(bnet)+'.0.0/16'
    OFILE=str(a_net)+'-'+str(bnet)+'-p80.log'
    A=subprocess.Popen(['masscan','-p80','-oG',OFILE,IPADDR,'--rate=2000'])
    A.wait()
    time.sleep(2)
    HADOOP_FILE_NAME='scans/'+str(a_net)+'/'+OFILE
    hdfs.put(OFILE,HADOOP_FILE_NAME)
    subprocess.Popen(['rm',OFILE])
