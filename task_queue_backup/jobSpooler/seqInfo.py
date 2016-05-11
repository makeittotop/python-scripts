#!/usr/bin/env python
import os
import sys
import re
from glob import *

__author__ = "Belal Salem <belal@nothing-real.com>"
__version__ = "1.02"

class seqInfo(object):
    '''
    seqInfo(seq, optional curFrame)
    where is:
    seq: arg is the sequence filename
        
    Returns:
        isSeq,        True:  if this is a sequence,
                             or a Padded file
                      False: otherwise
        baseDir,      Base Dir for the (seq)
        baseFileName, Base filename with neither extention
                      nor padding
        ext,          Sequence Extention
        pad,          Padding n
        start,        Sequence Start
        end,          Sequence End
        padPtrn,      The pattern %0?d
        padPtrn2,     The pattern ####
        padPtrn3,     The pattern ???? 'usefull when
                      searching for files in system'
        seqForm       The full sequence name in padPtrn
        seqForm2      The full sequence name in padPtrn2
        seqForm3      The full sequence name in padPtrn3
        file          The full filepath for a file at a given
                      frame number                  
        err           False if Ok,
                      str Error otherwise
                      
        Example:
        fileIn = seqInfo('/home/belal/snakeInSand.0001.ass')
        if fileIn.isSeq:
            print fileIn.baseDir
            print fileIn.baseFileName
            print fileIn.padPtrn
            print fileIn.seqExt
            print fileIn.padding
            print fileIn.seqStart
            print fileIn.seqEnd
    '''
    def __init__(self, seq, check=True, curFrame = -1):
        self.seq = str(seq)
        self.checkForSeq=check
        self.curFrame = int(curFrame)
        # Linux/OSX/Windows Compatiblity: (Don't know what exactly windows reports for platform)
        # The values in the 'if' statement may need modification on windows platforms 
        if os.name == 'posix':
            self.slash = '/'
        else:
            self.slash = '\\'
        
        
        # Initial the Data that should be returned
        self.isSeq = False
        self.baseDir = os.path.dirname(self.seq)
        self.baseFileName = os.path.basename(self.seq)
        self.padPtrn = ''
        self.padPtrn2 = ''
        self.padPtrn3 = ''
        self.ext = ''
        self.pad = False
        self.start = False
        self.end = False
        self.seqForm = ''
        self.seqForm2 = ''
        self.seqForm3 = ''
        self.file = ''
        self.err = False
        
        # Initial the file preparations
        seqFileIn = str(os.path.basename(str(self.seq)))
        self.firstSplit = str(os.path.splitext(seqFileIn)[0])
        self.secondSplit = str(os.path.splitext(self.firstSplit)[0])
        self.thirdSplit = str(os.path.splitext(self.secondSplit)[0])
        
        if self.checkForSeq:
            if len(self.firstSplit) < len(seqFileIn):
                # test if it's really an extention and not a SequenceNumber before setting seqExt
                # this helps solving < filename.%0nd > without extention
                testSeq = re.search(r'\d+$', seqFileIn)
                if not testSeq:
                    if self.secondSplit != self.thirdSplit: # Resolve double extentions sequences (filename.#.ext.gz)
                        self.ext =  os.path.splitext(str(os.path.splitext(seqFileIn)[0]))[1] + str(os.path.splitext(seqFileIn)[1])
                        self.baseFileName = self.thirdSplit
                        self.firstSplit = self.secondSplit
                        self.secondSplit = self.thirdSplit
                    else:
                        self.ext = os.path.splitext(seqFileIn)[1]
                        self.baseFileName = os.path.splitext(seqFileIn)[0]
                    
                else:
                    # This is a file sequence with dot, but without an extention
                    # < filename.# >
                    self.isSeq = True
                    self.ext = ''
                    self.pad = len(testSeq.group(0))
                    self.baseFileName = seqFileIn[:len(seqFileIn) - self.pad]
                    self.padPtrn = ''
                    for s in range(self.pad):
                        self.padPtrn += '#'      
            else:
                self.ext = ''        
            
            testSeq = re.search(r'\d+$', self.firstSplit)
            if testSeq:
                # It's a Sequence in pattern,
                # < filename_#.ext > or < filename#.ext >
                self.isSeq = True
                self.pad = len(testSeq.group(0))
                self.baseFileName = self.firstSplit[:len(self.firstSplit) - self.pad]
                self.padPtrn = '%' + str(self.pad).zfill(2) + 'd'
                self.padPtrn2 = ''
                self.padPtrn3 = ''
                for s in range(self.pad):
                    self.padPtrn2 += '#'
                for s in range(self.pad):
                    self.padPtrn3 += '?'
                self.seqForm = self.baseFileName + self.padPtrn + self.ext
                self.seqForm2 = self.baseFileName + self.padPtrn2 + self.ext
                self.seqForm3 = self.baseFileName + self.padPtrn3 + self.ext
                if self.curFrame != -1:
                    pad = str(self.curFrame).zfill(self.pad)
                    self.file = self.baseDir + self.slash + self.baseFileName + pad + self.ext
            
            # check the sequence on disk to collect
            # the rest needed info (start, end..)
            if len(str(self.pad)) == 1:
                # Force using '*' instead of '???..' in case of non-padded sequences
                seqPath = str(self.baseDir) + self.slash + self.baseFileName + '*' + self.ext
            else:    
                seqPath = str(self.baseDir) + self.slash + self.seqForm3
                
            seq = glob(seqPath)
            if seq and self.isSeq:
                for s in range(len(seq)):
                    seq[s] = int(seq[s][len(self.baseDir + self.slash + self.baseFileName):len(seq[s]) - len(self.ext)])
                    
                self.start = min(seq)
                self.end = max(seq)
                if self.start == self.end == 0:
                    # Force accepting single padded file, as file sequence with length of 1
                    x = re.search(r'\d+$', self.firstSplit)
                    if x:
                        x = x.group(0)
                        self.start = self.end = int(x)
                
            if self.isSeq and not seq:
                # Report an error code:
                self.err = "File sequence doesn't exist"
        
        else:
            # it may be a numbered file, but we want to treat it as single file
            # since checkForSeq is 'False'
            self.ext = os.path.splitext(seqFileIn)[1]
            self.baseFileName = self.firstSplit
            
