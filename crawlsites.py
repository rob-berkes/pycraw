import wget 
import time
  

ifp=open('54-149-p80.log','r')

for line in ifp:
  line = line.strip().split()
  url = 'http://'+str(line[1])+'/'
  time.sleep(3)
  
  try:
    wget.download(url,out='html/'+str(line[1])+'index.html')
  except IOError:
    continue
