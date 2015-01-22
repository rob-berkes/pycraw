#!/usr/bin/python
import sys
import re
for line in sys.stdin:
  line=line.strip().split()
  print line[5]
