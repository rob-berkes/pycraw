#!/usr/bin/python
import sys
import re
SUM=0
for line in sys.stdin:
    line=line.strip()
    SUM+=int(line)
print "Grand Total Corpus: "+str(SUM)
