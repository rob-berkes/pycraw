import wget 
import time
import urllib2
import socket
 

timeout = 8
socket.setdefaulttimeout(timeout)

ifp=open('54-149-p80.log','r')

for line in ifp:
  line = line.strip().split()
  url = 'http://'+str(line[1])+'/'
  req = urllib2.Request(url)
  html = ''
  try:
    html = urllib2.urlopen(req)
  except urllib2.HTTPError:
    pass
  except urllib2.URLError:
    pass
  
  print "-======= site: "+str(line[1])+" =======-"
  print html
 
#  try:
#    wget.download(url,out='html/'+str(line[1])+'index.html')
#  except IOError:
#    continue
