#!/usr/bin/python
import sys
import re
for line in sys.stdin:
  wordlist=re.findall(r"[\w']+",line)
  for word in  wordlist:
	print word

