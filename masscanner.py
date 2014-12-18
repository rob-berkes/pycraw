import subprocess 
for a in range(1,255):
  for b in range(1,255):
     if (a!=10) or ((a!=192) and(b!=168)) or ((a!=172) and(b!=16)):
       FNAME = 'scans/'+str(a)+'-'+str(b)+'-'+'-p80.log'
       SUBNET = str(a)+'.'+str(b)+'.'+'0.0/16'
       print 'scanning for net '+str(SUBNET)
       subprocess.call(['masscan','-p80','-oG',FNAME,SUBNET,'--rate=2000'])
