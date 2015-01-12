import subprocess
import pydoop.hdfs as hdfs

a_net=54
hdfs.mkdir(a_net)
for b_net in range(40,55):
    IPADDR=str(a_net)+'.'+str(bnet)+'.0.0/16'
    OFILE=str(a_net)+'-'+str(bnet)+'-p80.log'
    subprocess.call(['masscan','-p80','-oG',OFILE,IPADDR,'--rate=2000'])
    HADOOP_FILE_NAME='scans/'+str(a_net)+'/'+OFILE
    hdfs.put(OFILE
