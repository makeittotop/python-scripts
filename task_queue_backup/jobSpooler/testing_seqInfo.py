#!/usr/bin/env python
from seqInfo import *

d = '/home/belal/pyseq/tests/012_vb_110_v001.0007.png'
x = seqInfo(d)
print x.isSeq
print x.baseFileName
print x.pad
print x.ext
print x.start
print x.end
