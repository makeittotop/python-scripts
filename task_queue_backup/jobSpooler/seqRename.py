#!/usr/bin/env python

import sys
import os
import codecs
from os.path import isfile
from PyQt4 import QtCore, QtGui
from qRename_Win import Ui_RenameWinUI
from seqInfo import seqInfo

__author__ = "Belal Salem <belal@nothing-real.com>"
__version__ = "1.02"

class RenameQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_RenameWinUI()
        self.ui.setupUi(self)
        
        if os.name =='posix':
            # All unix systems should work with this:
            self.slash = '/'
            self.mvCmd = 'mv -f '
            self.cpCmd = 'cp -rf '
        else:
            self.slash = '\\'
            self.cpCmd = 'copy '
            # Not sure about the DOS command that is equivalent to 'mv' in unix systems,
            # the following may need to be replaced with 'rename ' to work correctly for windows platforms
            self.mvCmd = 'move '


        
        QtCore.QObject.connect(self.ui.browseNewSeqBtn, QtCore.SIGNAL("clicked()"), self.newSeqBrw)
        QtCore.QObject.connect(self.ui.browseDistSeqBtn, QtCore.SIGNAL("clicked()"), self.distSeqBrw)
        QtCore.QObject.connect(self.ui.renCpBtn, QtCore.SIGNAL("clicked()"), self.cpSeq)
        QtCore.QObject.connect(self.ui.renMvBtn, QtCore.SIGNAL("clicked()"), self.mvSeq)
        QtCore.QObject.connect(self.ui.qSeqOrig, QtCore.SIGNAL("textChanged(QString)"), self.seqChanged)
        #QtCore.QObject.connect(self.ui.qOrigSeqDir, QtCore.SIGNAL("textChanged(QString)"), self.seqChanged)
        
        # initialize original Seq Data
        self.task = False
        self.seqDir = False
        self.seqBaseName = False
        self.seqPad = False
        self.seqExt = False
        self.chosed = False

        # initialize Distination Seq Data
        self.distSeq = False
        self.distDir = False
        self.distBaseName = False
        self.distPad = False
        self.distExt = False
        self.autoDist = True
        self.autoDistDir = True
        self.srcTask = ''
        self.start = False
        self.end = False
        

        self.curDir = os.curdir

        # Parse Argv
        options = os.sys.argv[1:]
        argLen = len(options)
        if argLen > 0:
            if options[0] == '-mv':
                self.ui.renCpBtn.setEnabled(0)
            if options[0] == '-cp':
                self.ui.renMvBtn.setEnabled(0)
        if argLen > 1:
            if options[1]:
                self.ui.qOrigSeqDir.setText(os.path.dirname(options[1]))
                self.ui.qSeqOrig.setText(os.path.basename(options[1]))
                self.ui.qDistSeqDir.setText(os.path.dirname(options[1]))
                self.ui.qSeqDist.setText(os.path.basename(options[1]))

    def newSeqBrw(self):
        fd = QtGui.QFileDialog
        if self.seqDir:
            self.chosed = fd.getOpenFileName(caption = 'Get a sequence to Rename/Copy/Move ...', directory = self.seqDir, \
                                      filter = '*.*\n*.rib\n*.ass\n*.mi\n*.dpx\n*.exr\n*.tif\n*.sgi\n*.tga')
        else:
            self.chosed = fd.getOpenFileName(caption = 'Get a sequence to Rename/Copy/Move ...', directory = self.curDir, \
                                          filter = '*.*\n*.rib\n*.ass\n*.mi\n*.dpx\n*.exr\n*.tif\n*.sgi\n*.tga')
        if self.chosed:     
            task = str(os.path.join(str(os.path.dirname(str(self.chosed))), str(os.path.basename(str(self.chosed)))))
            self.ui.qOrigSeqDir.setText(os.path.dirname(task))
            self.ui.qSeqOrig.setText(str(os.path.basename(task)))
            
    def distSeqBrw(self):
        fd = QtGui.QFileDialog
        self.chosed = fd.getExistingDirectory(caption = 'Set a Destination folder ...', directory = self.curDir)
        if self.chosed:
            self.ui.qDistSeqDir.setText(self.chosed)
            self.autoDistDir = False
    
    def seqChanged(self):
        self.autoDist = True
        self.seqDir = self.ui.qOrigSeqDir.text() + self.slash
        self.seqBaseName = self.ui.qSeqOrig.text()
        self.task = str(self.seqDir + self.seqBaseName)
        self.srcTask = seqInfo(self.task)
        if self.srcTask.isSeq:
            self.start = self.srcTask.start
            self.end = self.srcTask.end
            if self.autoDistDir:
                self.ui.qDistSeqDir.setText(os.path.dirname(self.task))
            self.ui.qSeqDist.setText(os.path.basename(self.task))
            self.ui.qTimeRange.setText(str(self.start) + ' : ' + str(self.end))
            
        else:
            # Raise an Error Message:
            # Cannot work for single file, if you are sure it's a sequence
            # check what's wrong with your source selected file!
            pass
        
    def seqDirChanged(self):
        if self.autoDist:
            self.newSeq = os.path.join(str(self.ui.qSeqOrig.text())) 
            self.ui.qSeqDist.setText(self.newSeq)
            
    def mvSeq(self):
        if not self.srcTask.err and self.srcTask.isSeq:
            for s in range(self.start, self.end+1):
                targetSeq = seqInfo(os.path.join(str(self.ui.qOrigSeqDir.text()), str(self.ui.qSeqDist.text())))
                srcPad = str(s).zfill(self.srcTask.pad)
                distPad = str(s).zfill(targetSeq.pad)
                target = targetSeq.baseDir + self.slash + targetSeq.baseFileName + distPad + targetSeq.ext
                source = self.srcTask.baseDir +  self.slash + self.srcTask.baseFileName + srcPad + self.srcTask.ext
                os.system(self.mvCmd + source + ' ' + target)
                self.ui.qTimeRange.setText(str(s) + ' : ' + str(self.srcTask.end))
            self.ui.qTimeRange.setText('DONE')
            distPad = str(targetSeq.start).zfill(targetSeq.pad)
            newPattern = targetSeq.baseDir + self.slash + targetSeq.baseFileName + distPad + targetSeq.ext
            Dismiss = 'Dismiss'
            message = QtGui.QMessageBox(self)
            message.setText("You may want to copy the new sequence pattern!\n" + newPattern)
            message.setWindowTitle('jobSpooler...')
            message.setIcon(QtGui.QMessageBox.Information)
            message.addButton(Dismiss, QtGui.QMessageBox.AcceptRole)
            message.exec_()
            clipboard = QtGui.QApplication.clipboard().text()
            print clipboard
        else:
            self.renderCmd = False
            Dismiss = 'Dismiss'
            message = QtGui.QMessageBox(self)
            message.setText("Sorry! Single files are not supported!\nYou can just use the system for this!")
            message.setWindowTitle('jobSpooler...')
            message.setIcon(QtGui.QMessageBox.Warning)
            message.addButton(Dismiss, QtGui.QMessageBox.AcceptRole)
            message.exec_()

                
    
    def cpSeq(self):
        if not self.srcTask.err and self.srcTask.isSeq:
            for s in range(self.start, self.end+1):
                targetSeq = seqInfo(os.path.join(str(self.ui.qOrigSeqDir.text()), str(self.ui.qSeqDist.text())))
                srcPad = str(s).zfill(self.srcTask.pad)
                distPad = str(s).zfill(targetSeq.pad)
                target = targetSeq.baseDir +  self.slash + targetSeq.baseFileName + distPad + targetSeq.ext
                source = self.srcTask.baseDir +  self.slash + self.srcTask.baseFileName + srcPad + self.srcTask.ext
                os.system(self.cpCmd + source + ' ' + target)
                self.ui.qTimeRange.setText(str(s) + ' : ' + str(self.srcTask.end))
            self.ui.qTimeRange.setText('DONE')
        else:
            self.renderCmd = False
            Dismiss = 'Dismiss'
            message = QtGui.QMessageBox(self)
            message.setText("Sorry! Single files are not supported!\nYou can just use the system for this!")
            message.setWindowTitle('jobSpooler...')
            message.setIcon(QtGui.QMessageBox.Warning)
            message.addButton(Dismiss, QtGui.QMessageBox.AcceptRole)
            message.exec_()
            #response = message.clickedButton().text()              
        
if __name__ == '__main__':
    renSeqApp = QtGui.QApplication(sys.argv)
    myRenSeq = RenameQT4()
    myRenSeq.show()
    sys.exit(renSeqApp.exec_())