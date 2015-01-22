#!/usr/bin/python
import sys
import re
line = sys.stdin.readline()
wordlist=re.findall(r"[\w+]",line)
print len(wordlist)


