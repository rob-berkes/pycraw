#!/usr/bin/python
import sys
import re
SUM=0
#wordlist = re.findall(r"[\w']+",line)
for line in sys.stdin:
    SUM+=1
print "The total number of words: "+str(SUM)
