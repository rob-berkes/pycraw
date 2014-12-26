import subprocess
anet=54
for bnet in range(40,55):
    IPADDR=str(anet)+'.'+str(bnet)+'.0.0/16'
    OFILE='scans/'+str(anet)+'-'+str(bnet)+'--p80.log'
    subprocess.call(['masscan','-p80','-oG',OFILE,IPADDR,'--rate=2000'])
