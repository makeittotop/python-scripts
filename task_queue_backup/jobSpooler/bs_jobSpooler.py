#!/usr/bin/env python

import sys
import os
import codecs
from PyQt4 import QtCore, QtGui
from bs_pipeline.jobSpooler.qjobSpooler_UI import Ui_qSpooler
from bs_pipeline.jobSpooler.seqInfo import seqInfo
import re, glob

import rfm.tractor

try:
    from maya import OpenMayaUI as omui
    import maya.cmds as cmds
    from pymel.core import *
    import sip
except:
    pass

__author__ = "Belal Salem <belal@nothing-real.com>"
__version__ = "1.6.5"

# Global Variables Initialization
WINDOW_TITLE = 'Tractor/Alfred Job Spooler'
WINDOW_VERTION = __version__
WINDOW_NAME = 'qSpooler'


def mayaMainWindow():
    try:
        mayaWinPtr = omui.MQtUtil.mainWindow()
        mayaWin = sip.wrapinstance(long(mayaWinPtr), QtGui.QWidget)
        return mayaWin
    except:
        return None


class jobSpooler(QtGui.QDialog):
    def __init__(self, parent=mayaMainWindow(), imgPath=None, tskType=0, tskFile=False, prjPath=False, tskScript='', opt='',
                title='', start=False, end=False, priority=50, taskSize=1, standalone=True):
        #QtGui.QWidget.__init__(self, parent)
        super(jobSpooler, self).__init__(parent)
        self.ui = Ui_qSpooler()
        self.ui.setupUi(self)

        # Initial variables:
        self.checkForSeq = False

        if os.name == 'posix':
            self.slash = '/'
            self.tsr = '&'
        else:
            self.slash = '\\'
            self.tsr = '&'  # Not sure what is equivalent to this under windows

        self.setWindowTitle('{0} {1}'.format(WINDOW_TITLE, str(WINDOW_VERTION)))
        
        engineVar = os.getenv('TRACTOR_ENGINES')
        if engineVar != None:
            engines = []
            enginesParts = engineVar.split(':')

            eng = '%s:%s'%(enginesParts[2], enginesParts[3])
            engines.append(eng)
            self.ui.engineTxt.addItem(eng)
            self.engine = eng

            '''
            if len(engines) % 2 == 0:
                for i in xrange(0, len(enginesParts), 2):

                    if enginesParts[i] == 'lic':
                        next

                    eng = '%s:%s'%(enginesParts[i], enginesParts[i+1])
                    engines.append(eng)
                    self.ui.engineTxt.addItem(eng)
                self.engine = '%s:%s'%(enginesParts[0], enginesParts[1])    #set self.engine to first available engine
            else:
                print 'warning: TRACTOR_ENGINES var should be set as engine:port pairs, default engine will be used.'
                self.engine = 'tractor-engine:80'
                self.ui.engineTxt.addItem(self.engine)
            '''
        else:
            print 'warning: TRACTOR_ENGINES var was not set, default engine will be used.'
            self.engine = 'tractor-engine:80'
            self.ui.engineTxt.addItem(self.engine)
        
        QtCore.QObject.connect(self.ui.prjPathBtn, QtCore.SIGNAL("clicked()"), self.browsePrj)
        QtCore.QObject.connect(self.ui.browseSeqBtn, QtCore.SIGNAL("clicked()"), self.browseSeq)
        QtCore.QObject.connect(self.ui.browseScriptBtn, QtCore.SIGNAL("clicked()"), self.browseScript)
        QtCore.QObject.connect(self.ui.alfredBtn, QtCore.SIGNAL("clicked()"), self.sendAlfred)
        QtCore.QObject.connect(self.ui.tractorBtn, QtCore.SIGNAL("clicked()"), self.sendToTractor)
        QtCore.QObject.connect(self.ui.genTaskBtn, QtCore.SIGNAL("clicked()"), self.preGen)
        QtCore.QObject.connect(self.ui.renCpBtn, QtCore.SIGNAL("clicked()"), self.renCp)
        QtCore.QObject.connect(self.ui.renMvBtn, QtCore.SIGNAL("clicked()"), self.renMv)
        QtCore.QObject.connect(self.ui.renderBtn, QtCore.SIGNAL("clicked()"), self.render)
        QtCore.QObject.connect(self.ui.qTaskType, QtCore.SIGNAL("currentIndexChanged(QString)"), self.Task)
        QtCore.QObject.connect(self.ui.engineTxt, QtCore.SIGNAL("currentIndexChanged(QString)"), self.engChanged)
        QtCore.QObject.connect(self.ui.engineTxt, QtCore.SIGNAL("currentTextEdited(QString)"), self.engChanged)
        QtCore.QObject.connect(self.ui.qTaskSeq, QtCore.SIGNAL("textChanged(QString)"), self.taskSeq)
        QtCore.QObject.connect(self.ui.qPrjPath, QtCore.SIGNAL("textChanged(QString)"), self.setPrj)
        QtCore.QObject.connect(self.ui.taskTitle, QtCore.SIGNAL("textChanged(QString)"), self.title)
        QtCore.QObject.connect(self.ui.qScriptPath, QtCore.SIGNAL("editingFinished()"), self.scriptHandPath)
        QtCore.QObject.connect(self.ui.autoStart, QtCore.SIGNAL("toggled(bool)"), self.checkToggled)
        QtCore.QObject.connect(self.ui.autoEnd, QtCore.SIGNAL("toggled(bool)"), self.checkToggled)
        QtCore.QObject.connect(self.ui.seqFrom, QtCore.SIGNAL("editingFinished()"), self.unCheckStart)
        QtCore.QObject.connect(self.ui.seqTo, QtCore.SIGNAL("editingFinished()"), self.unCheckEnd)
        QtCore.QObject.connect(self.ui.engineTxt, QtCore.SIGNAL("editingFinished()"), self.engineMod)
        QtCore.QObject.connect(self.ui.periorityTxt, QtCore.SIGNAL("editingFinished()"), self.priorityChange)
        QtCore.QObject.connect(self.ui.perTask, QtCore.SIGNAL("editingFinished()"), self.taskSizeChange)
        QtCore.QObject.connect(self.ui.curLayerBtn, QtCore.SIGNAL("clicked()"), self.onlyCurLayer)

        self.priority = priority
        self.taskSize = 1
        self.standalone = standalone
        self.curDir = os.path.abspath(os.curdir)
        self.prjPathDone = False
        self.scriptAutoNamed = True
        self.jobFile = False
        self.jobScript = tskScript
        self.prjPath = False
        self.curDir = os.path.abspath(os.curdir)
        self.taskDir = False
        self.taskBaseName = False
        self.singleTaskFile = False
        self.job = False
        self.fileSeq = False
        self.seqName = False
        self.taskStart = False
        self.prjPath = self.curDir
        self.genMsgEnabled = True
        self.renderCmd = 'kickMaya -nstdin '
        self.err = False
        self.curLayer = False
        self.imgPath = imgPath

        # parse arguments
        self.ui.qTaskType.setCurrentIndex(tskType)
        self.Task()
        if tskFile:
            self.ui.qTaskSeq.setText(tskFile)
        if prjPath:
            self.ui.qPrjPath.setText(prjPath)
            self.prjPathDone = True
        if title:
            self.ui.taskTitle.setText(title)
        if opt:
            self.ui.optionalArgs.setText(opt)
        if start > 0:
            self.ui.seqFrom.setValue(start)
            self.taskStart = start
        if end > 0:
            self.ui.seqTo.setValue(end)
            self.taskEnd = end
        if taskSize > 1:
            self.ui.perTask.setValue(taskSize)
            self.taskSize = taskSize
        if priority != 50:
            self.ui.periorityTxt.setValue(priority)
            self.priority = priority

        self.extraArgs = ' ' + opt
        self.jobFullPath = tskScript
        self.task = seqInfo(tskFile, False)
        self.prjPath = prjPath
        self.tskStart = start
        self.taskEnd = end
        self.taskFile = tskFile
    
    def engChanged(self):
        self.engine = self.ui.engineTxt.currentText()
    
    def Task(self):   # qTaskType index Names
        self.taskIndex = self.ui.qTaskType.currentIndex()
        if self.taskIndex == 0:   # Arnold Render
            self.taskExt = '.ass'
            self.taskExtGz = '.ass.gz'
            self.renderCmd = 'kickMaya -nstdin '
            self.ui.patchBtn.setText('Patch ASS')
            self.ui.patchBtn.setEnabled(1)
            self.ui.renCpBtn.setEnabled(1)
            self.ui.renMvBtn.setEnabled(1)
            self.ui.renderBtn.setEnabled(1)
            self.ui.curLayerBtn.setEnabled(0)
            self.checkForSeq = True
            return

        if self.taskIndex == 1:   # Renderman Render
            self.taskExt = '.rib'
            self.taskExtGz = '.rib.gz'
            self.renderCmd = 'prman -d it '
            self.ui.patchBtn.setText('Patch RIBs')
            self.ui.patchBtn.setEnabled(1)
            self.ui.renCpBtn.setEnabled(1)
            self.ui.renMvBtn.setEnabled(1)
            self.ui.renderBtn.setEnabled(1)
            self.ui.curLayerBtn.setEnabled(0)
            self.checkForSeq = True
            return

        if self.taskIndex == 2:   # Massive Simulation
            self.taskExt = '.mas'
            self.taskExtGz = ''
            self.ui.patchBtn.setText('Patch Mas')
            self.ui.patchBtn.setEnabled(1)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            self.checkForSeq = False
            return

        if self.taskIndex == 3:   # Katana Render
            self.taskExt = '.katana'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            self.checkForSeq = False
            return

        if self.taskIndex == 4:   # Nuke Render
            self.taskExt = '.nk'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.checkForSeq = False
            self.ui.curLayerBtn.setEnabled(0)
            return

        if self.taskIndex == 5:   # Maya Render
            self.taskExt = '.ma *.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.checkForSeq = False
            if not self.standalone:
                self.ui.curLayerBtn.setEnabled(1)
            return

        if self.taskIndex == 6:   # Maya Cmd Script
            self.taskExt = '.ma *.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            self.checkForSeq = False
            return

        if self.taskIndex == 7:   # Mentalray Render
            self.taskExt = '.mi'
            self.taskExtGz = ''
            self.ui.patchBtn.setText('Patch Mi')
            self.ui.patchBtn.setEnabled(1)
            self.ui.renCpBtn.setEnabled(1)
            self.ui.renMvBtn.setEnabled(1)
            self.ui.renderBtn.setEnabled(1)
            self.ui.curLayerBtn.setEnabled(0)
            self.checkForSeq = True
            return
        
        if self.taskIndex == 8:   # FumeFX Sim
            self.taskExt = '.ma *.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.checkForSeq = False
            if not self.standalone:
                self.ui.curLayerBtn.setEnabled(1)
            return
        
        if self.taskIndex == 9:   # FumeFX Render
            self.taskExt = '.ma *.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.checkForSeq = False
            if not self.standalone:
                self.ui.curLayerBtn.setEnabled(1)
            return

        if self.taskIndex > 9:
            self.renderCmd = False
            Confirm = 'Confirm'
            message = QtGui.QMessageBox(self)
            message.setText("Sorry! This task type is not implemented yet.\n Check for updates from www.nothing-real.com")
            message.setWindowTitle('jobSpooler...')
            message.setIcon(QtGui.QMessageBox.Warning)
            message.addButton(Confirm, QtGui.QMessageBox.AcceptRole)
            message.exec_()
            self.ui.curLayerBtn.setEnabled(0)
            return
            # response = message.clickedButton().text()

        if self.taskIndex == 10:   # Renderman RIB Generate
            self.taskExt = '.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            return

        if self.taskIndex == 11:   # Arnold ASS Generate
            self.taskExt = '.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            return

        if self.taskIndex == 12:   # Mentalray MI gen
            self.taskExt = '.mb'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            return

        if self.taskIndex == 13:   # Fusion Render
            self.taskExt = '.comp'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            return

        if self.taskIndex == 14:   # Shake Render
            self.taskExt = '.shk'
            self.taskExtGz = ''
            self.ui.patchBtn.setEnabled(0)
            self.ui.renCpBtn.setEnabled(0)
            self.ui.renMvBtn.setEnabled(0)
            self.ui.renderBtn.setEnabled(0)
            self.ui.curLayerBtn.setEnabled(0)
            return

    def browsePrj(self):
        fd = QtGui.QFileDialog(self)
        newPrjPath = fd.getExistingDirectory(caption='Set Project Path', directory=self.curDir)
        if newPrjPath:
            self.prjPath = newPrjPath
            self.ui.qPrjPath.setText(self.prjPath)
            if self.scriptAutoNamed:
                self.curDir = self.ui.qPrjPath.text()

    def setPrj(self):
        self.prjPath = self.ui.qPrjPath.text()
        self.prjPathDone = True
        if self.scriptAutoNamed:
            self.curDir = self.prjPath
            self.title()

    def browseSeq(self):
        fd = QtGui.QFileDialog(self)
        #fd.setNameFilter('*.* *.ass')
        curDir = str(self.ui.qTaskSeq.text())

        if not self.prjPath:
            self.prjPath = curDir

        if not self.taskExtGz == '':
            if curDir:
                self.seqName = fd.getOpenFileName(caption='Get a Task File ...', directory=curDir, filter='*' +
                            str(self.taskExt + '\n*' + self.taskExtGz + '\n*.*'))
            else:
                self.seqName = fd.getOpenFileName(caption='Get a Task File ...', directory=self.prjPath, filter='*' +
                            str(self.taskExt + '\n*' + self.taskExtGz + '\n*.*'))
        else:
            if curDir:
                self.seqName = fd.getOpenFileName(caption='Get a Task File ...', directory=curDir, filter='*' +
                            str(self.taskExt + '\n*.*'))
            else:
                self.seqName = fd.getOpenFileName(caption='Get a Task File ...', directory=self.prjPath, filter='*' +
                            str(self.taskExt + '\n*.*'))
        if self.seqName:
            self.ui.qTaskSeq.setText(self.seqName)

    def taskSeq(self):
        self.seqName = str(self.ui.qTaskSeq.text())

        self.task = seqInfo(self.seqName, self.checkForSeq)

        if self.task.isSeq:
            if not self.ui.autoStart.isEnabled():
                # Re enable 'auto' checkboxes after recovering from a singled file task
                self.ui.seqFrom.setValue(self.task.start)
                self.ui.seqTo.setValue(self.task.end)
                self.ui.autoStart.setEnabled(1)
                self.ui.autoStart.setChecked(1)
                self.ui.autoEnd.setEnabled(1)
                self.ui.autoEnd.setChecked(1)
            else:
                if self.ui.autoStart.isChecked():
                    self.ui.seqFrom.setValue(int(self.task.start))
                if self.ui.autoEnd.isChecked():
                    self.ui.seqTo.setValue(int(self.task.end))
        else:
            # Single Frame
            self.ui.seqFrom.setValue(0)
            self.ui.seqTo.setValue(0)
            self.ui.autoStart.setChecked(0)
            self.ui.autoEnd.setChecked(0)
            self.ui.autoStart.setEnabled(0)
            self.ui.autoEnd.setEnabled(0)

        if re.search(r'\.+$', self.task.baseFileName) or re.search(r'\_+$', self.task.baseFileName):
            self.ui.taskTitle.setText(self.task.baseFileName[:-1])
        else:
            self.ui.taskTitle.setText(self.task.baseFileName)

        if not self.prjPathDone:
            self.curDir = self.task.baseDir
            self.ui.qPrjPath.setText(self.curDir)
            self.prjPathDone = True
    
    def onlyCurLayer(self):
        curLayer = editRenderLayerGlobals(q=True, crl=True)
        optArgs = self.ui.optionalArgs.toPlainText()
        optArgs = '-l %s '%curLayer + optArgs
        self.ui.optionalArgs.setPlainText(optArgs)
        jobTitle = self.ui.taskTitle.text() + '_%s'%curLayer
        self.ui.taskTitle.setText(jobTitle)
    
    def errorCheck(self):
        self.seqName = str(self.ui.qTaskSeq.text())
        self.task = seqInfo(self.seqName, self.checkForSeq)
        if self.task.err:
            Confirm = 'Confirm'
            Cancel = 'Cancel'
            message = QtGui.QMessageBox(self)
            message.setText("The task sequence provided doesn't seem to be exist!")
            message.setWindowTitle('jobSpooler...')
            message.setIcon(QtGui.QMessageBox.Warning)
            message.addButton(Confirm, QtGui.QMessageBox.AcceptRole)
            message.addButton(Cancel, QtGui.QMessageBox.RejectRole)
            message.exec_()
            response = message.clickedButton().text()
            if response == Confirm:
                self.err = False
            else:
                self.err = True

    def checkToggled(self):
        self.seqName = str(self.ui.qTaskSeq.text())
        self.task = seqInfo(self.seqName, self.checkForSeq)
        if self.task.isSeq:
            if not self.ui.autoStart.isEnabled():
                # Re enable 'auto' checkboxes after recovering from a singled file task
                self.ui.seqFrom.setValue(self.task.start)
                self.ui.seqTo.setValue(self.task.end)
                self.ui.autoStart.setEnabled(1)
                self.ui.autoStart.setChecked(1)
                self.ui.autoEnd.setEnabled(1)
                self.ui.autoEnd.setChecked(1)
            else:
                if self.ui.autoStart.isChecked():
                    self.ui.seqFrom.setValue(int(self.task.start))
                if self.ui.autoEnd.isChecked():
                    self.ui.seqTo.setValue(int(self.task.end))
        else:
            # Single Frame
            self.ui.seqFrom.setValue(0)
            self.ui.seqTo.setValue(0)
            self.ui.autoStart.setChecked(0)
            self.ui.autoEnd.setChecked(0)
            self.ui.autoStart.setEnabled(0)
            self.ui.autoEnd.setEnabled(0)

    def browseScript(self):
        fd = QtGui.QFileDialog(self)
        if self.ui.taskTitle.text():
            tmpName = fd.getSaveFileName(caption='Set "Task Script" name:', directory=self.ui.taskTitle.text()
                                         + '.alf', filter='*.alf\n*.*')
        else:
            tmpName = fd.getSaveFileName(caption='Set "Task Script" name:', directory='untitled.alf',
                                         filter='*.alf\n*.*')
        if tmpName:   # SAVE Clicked
            self.scriptAutoNamed = False
            self.curDir = os.path.dirname(str(tmpName))
            self.jobFile = tmpName
            self.ui.qScriptPath.setText(self.jobFile)

    def engineMod(self):
        self.engine = self.ui.engineTxt.text()

    def priorityChange(self):
        self.priority = self.ui.periorityTxt.value()

    def taskSizeChange(self):
        self.taskSize = self.ui.perTask.value()

    def unCheckStart(self):
        self.ui.autoStart.setChecked(0)

    def unCheckEnd(self):
        self.ui.autoEnd.setChecked(0)

    def title(self):
        if self.ui.taskTitle.text():
            self.jobFile = str(self.curDir) + self.slash + self.ui.taskTitle.text() + '.alf'
        else:
            self.jobFile = str(self.curDir) + self.slash + 'untitled.alf'
        self.ui.qScriptPath.setText(self.jobFile)
        self.jobScript = str(self.ui.qScriptPath.text())

    def scriptHandPath(self):
        self.curDir = os.path.dirname(str(self.ui.qScriptPath.text()))
        self.scriptAutoNamed = False

    def preGen(self):
        self.errorCheck()
        if not self.err:
            self.genTask()

    def genTask(self, internal=True):
        if internal:
            # Preparing:
            dataIsOk = False
            header = False
            exArgs = self.ui.optionalArgs.toPlainText()
            extraArgs = ' ' + exArgs
            self.jobFullPath = str(self.ui.qScriptPath.text())
            taskBaseFilename = self.task.baseFileName
            taskPrj = str(self.prjPath)
            taskDir = self.task.baseDir
            relativeDir = os.path.relpath(taskDir, taskPrj) + self.slash
            jobStart = int(self.ui.seqFrom.value())
            jobEnd = int(self.ui.seqTo.value())
            job = ''
            g = codecs.open(self.jobFullPath, 'w', 'utf-8')
            absTaskPath = str(self.ui.qTaskSeq.text())
            self.taskEnd = self.ui.seqTo.value()
                            
            if self.task.isSeq or 2 < self.taskIndex < 6 or 7 < self.taskIndex < 10:
                # Preparing for Sequencial Task
                jobRange = range(jobStart, jobEnd + 1)
                #taskBaseFilename += '.'
            else:
                # Preparing for Singled Task
                jobRange = range(1, 2)
        else:
            # Preparing:
            dataIsOk = False
            header = False
            extraArgs = self.extraArgs
            taskBaseFilename = self.task.baseFileName
            taskPrj = self.prjPath
            taskDir = self.task.baseDir
            relativeDir = os.path.relpath(taskDir, taskPrj) + self.slash
            jobStart = int(self.tskStart)
            jobEnd = int(self.taskEnd)
            job = ''
            g = codecs.open(self.jobFullPath, 'w', 'utf-8')
            absTaskPath = self.taskFile
            self.taskEnd = self.taskEnd

            if self.task.isSeq or 2 < self.taskIndex < 6 or 7 < self.taskIndex < 10:
                # Preparing for Sequencial Task
                jobRange = range(jobStart, jobEnd + 1)
                #taskBaseFilename += '.'
            else:
                # Preparing for Singled Task
                jobRange = range(1, 2)
        
        # Setting imgPath (for preview frame of maya jobs)
        try:
            iP = os.path.dirname(getAttr('defaultRenderGlobals.imageFilePrefix'))
            if len(iP.split('<RenderLayer>')) > 1:
                curLayer = editRenderLayerGlobals(q=True, crl=True)
                iP = iP.split('<RenderLayer>')[0] + curLayer + '/'
        except:
            iP = None
        
        if self.imgPath is not None:
            iP = self.imgPath           # override imagePath above if been passed through the spooler caller

        # Preparing blade profiles specifics:
        extraService = ""
        if self.ui.profilesBox.currentIndex() == 1:
            extraService = " && highMem &! preview"

        elif self.ui.profilesBox.currentIndex() == 2:
            extraService = " && preview "

        elif self.ui.profilesBox.currentIndex() == 3:
            extraService = " && external &! preview"
        
        elif self.ui.profilesBox.currentIndex() == 4:
            extraService = " && highMem && external &! preview"
        
        elif self.ui.profilesBox.currentIndex() == 5:
            extraService = " && fumeFX"
        
        elif self.ui.profilesBox.currentIndex() == 6:
            extraService = " && comp" # empty will take only Nuke service key
            
        # OK! Here we are ready to generate the task
        counter = jobStart
        for s in jobRange:
            relativeTaskPath = relativeDir + taskBaseFilename
            if self.task.isSeq:
                paddedS = str(s)
                paddedS = paddedS.zfill(self.task.pad)
                relativeTaskPath += paddedS + self.task.ext
            #elif self.taskIndex == 3:
            #    paddedS = str(s)
            #    paddedS = paddedS.zfill(4)
            #    relativeTaskPath = self.slash + taskBaseFilename + self.task.ext
            #    subtaskTitle = '{Processing frame ' + str(s) + '} '
            else:
                paddedS = str(s).zfill(4)

            # subTask title should be like this except for Massive and Naiad
            subtaskTitle = '{Processing ' + str(s) + '} '
            atleast = '-atleast %s' % str(self.ui.atleastSpin.value())
            atMost = '-atmost %s' % str(self.ui.atmostSpin.value())
            sameHost = '-samehost %s' % str(self.ui.samehostSpin.value())
            slotOpt = '%s %s %s ' % (sameHost, atleast, atMost)
            
            # Setting any Task Type specific Data
            if self.taskIndex == 0:
                # Arnold Render Task
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskArgs = '-dw -dp -v 3 -nstdin -nokeypress -nw 3 -i '
                taskCmd = 'kickAss '
                service = '"kick%s" %s' %(extraService, slotOpt)
                tag = '{kick}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' \
                                    + paddedS + '.exr}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' \
                                    + paddedS + '.exr}'
                oneRange = ''
                dataIsOk = True

            elif self.taskIndex == 1:
                # Renderman Render Task
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskArgs = '-Progress -cwd '
                taskCmd = 'prman '
                service = '"PixarRender%s" %s' %(extraService, slotOpt)
                tag = '{prman}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] \
                                     + '.' + paddedS + '.tif}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename \
                                    + '.' + paddedS + '.tif}'
                oneRange = ''
                dataIsOk = True

            elif self.taskIndex == 2:
                # Massive Crowd Simulation
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Simulating ' + str(jobStart) + '-' + str(jobEnd) + '} '
                subtaskTitle = taskTitle
                taskArgs = '-gui -alf -v -sim '
                taskCmd = 'crowdSim '
                service = '"massive%s" %s' %(extraService, slotOpt)
                tag = '{massive}'
                imagePreview = ''
                oneRange = str(jobStart) + '-' + str(jobEnd) + ' '
                dataIsOk = True

            elif self.taskIndex == 3:
                # Katana Batch Render
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskCmd = 'katanaRen '
                taskArgs = '--batch -t '
                service = '"katana%s" %s' %(extraService, slotOpt)
                tag = '{katana}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' + paddedS + '.exr}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' + paddedS + '.exr}'
                oneRange = str(s) + ' '
                dataIsOk = True

            elif self.taskIndex == 4:
                # Nuke Batch Render
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskCmd = '/usr/local/Nuke7.0v10/Nuke7.0 '
                taskArgs = '-f -t '
                service = '"nuke%s" %s' %(extraService, slotOpt)
                tag = '{nuke}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' + paddedS + '.exr}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' + paddedS + '.exr}'
                oneRange = str(s) + ' '
                dataIsOk = True

            elif self.taskIndex == 5:
                # Maya Batch Render
                mayaLocation = os.getenv('MAYA_LOCATION')
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskCmd = '%s/bin/Render '%mayaLocation
                taskArgs = ''
                service = '"PixarRender%s" %s' %(extraService, slotOpt)
                tag = '{prman}'
                if taskBaseFilename[-1:] == '.':
                    if iP is None:
                        imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' + paddedS + '.exr}'
                    else:
                        imagePreview = '-preview {rv ' + iP + 'beauty_' + taskBaseFilename[:-1] + '.' + paddedS + '.exr}'
                else:
                    if iP is None:
                        imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' + paddedS + '.exr}'
                    else:
                        imagePreview = '-preview {rv ' + iP + 'beauty_' + taskBaseFilename + '.' + paddedS + '.exr}'
                oneRange = str(s) + ' '
                dataIsOk = True

            elif self.taskIndex == 6:
                # Maya Batch run command 'Maya script'
                mayaLocation = os.getenv('MAYA_LOCATION')
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskCmd = '%s/bin/maya -batch '%mayaLocation
                taskArgs = ''
                service = '"PixarRender%s" %s' %(extraService, slotOpt)
                tag = '{prman}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' + paddedS + '.exr}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' + paddedS + '.exr}'
                oneRange = str(s) + ' '
                dataIsOk = True
            
            elif self.taskIndex == 8:
                # FumeFX Simulate
                mayaLocation = os.getenv('MAYA_LOCATION')
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskCmd = '%s/bin/Render '%mayaLocation
                taskArgs = ''
                service = '"PixarRender%s" %s' %(extraService, slotOpt)
                tag = '{prman}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' + paddedS + '.exr}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' + paddedS + '.exr}'
                oneRange = str(s) + ' '
                dataIsOk = True
            
            elif self.taskIndex == 9:
                # FumeFX Render
                mayaLocation = os.getenv('MAYA_LOCATION')
                jobComment = '{# Created by Belal Salem through jobSpooler} '
                jobTitle = '{' + str(self.ui.taskTitle.text()) + '} '
                taskTitle = '{Renders ' + str(jobStart) + '-' + str(jobEnd) + '} '
                taskCmd = '%s/bin/Render '%mayaLocation
                taskArgs = ''
                service = '"PixarRender%s" %s' %(extraService, slotOpt)
                tag = '{prman}'
                if taskBaseFilename[-1:] == '.':
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename[:-1] + '_beauty.' + paddedS + '.exr}'
                else:
                    imagePreview = '-preview {sho ' + taskPrj + self.slash + 'images' + self.slash + taskBaseFilename + '_beauty.' + paddedS + '.exr}'
                oneRange = str(s) + ' '
                dataIsOk = True

            else:
                pass

            if not header:
                header = True
                if not self.task.isSeq:
                    relativeTaskPath += self.task.ext
                job += '##AlfredToDo 3.0' + '\n'
                job += 'Job -title ' + jobTitle + '-comment ' + jobComment + '-serialsubtasks 0 -pbias %s -subtasks {'%str(self.priority)+ '\n'
                job += '    Task -title ' + taskTitle + '-serialsubtasks 0 -subtasks {' + '\n'

            if self.taskIndex == 5 or self.taskIndex == 9:
                processingEnd = counter+self.taskSize-1
                if processingEnd > self.taskEnd:
                    processingEnd = self.taskEnd
                subtaskTitle = '{Processing ' + str(counter) + '-' + str(processingEnd)+ '} '
                if counter <= (self.taskEnd):
                    job     += '        Task -title ' + subtaskTitle + '-cmds {' + '\n'
                else:
                    break
            else:
                job         += '        Task -title ' + subtaskTitle + '-cmds {' + '\n'

            if self.taskIndex == 3: # katana treated differently
                            job     += '            RemoteCmd {' + taskCmd + extraArgs + ' ' + taskArgs + oneRange + absTaskPath + \
                                            ' } -service ' + service + '-tags ' + tag + '\n'
            if self.taskIndex == 4: # Nuke treated differently
                stFrame = str(counter)
                endFrame = int(counter) + self.taskSize - 1
                if endFrame > self.taskEnd:
                    endFrame = self.taskEnd
                endFrame = str(endFrame)
                counter += self.taskSize
                job                 += '            RemoteCmd {' + taskCmd + extraArgs + ' ' + taskArgs + '-x ' + absTaskPath + ' %s-%s'%(stFrame, endFrame) +\
                                            ' } -service ' + service + '-tags ' + tag + '\n'
            elif self.taskIndex == 5 or self.taskIndex == 9: # Maya and FumeFX Render through Maya have also different treatement
                stFrame = str(counter) + ' '
                endFrame = int(counter) + self.taskSize - 1
                if endFrame > self.taskEnd:
                    endFrame = self.taskEnd
                endFrame = str(endFrame)
                counter += self.taskSize
                job                 += '            RemoteCmd {' + taskCmd + '-s ' + stFrame + '-e ' + endFrame + extraArgs + ' ' + taskArgs + '-proj ' + taskPrj + ' ' + absTaskPath + \
                                            ' } -service ' + service + '-tags ' + tag + '\n'
            else:
                if self.taskIndex != 3:
                    job += '            RemoteCmd {' + taskCmd + extraArgs + ' ' + taskArgs + oneRange + taskPrj + ' ' + relativeTaskPath + \
                                                ' } -service ' + service + '-tags ' + tag + '\n'
            job     += '        } ' + imagePreview + '\n'
        job         += '    }' + '\n'
        job         += '}' + '\n'


        #Write job to the file and close
        if dataIsOk:
            g.write(unicode(job))
            g.close()
            print >>sys.stdout, "Job Generated Successfully! Thanks for using 'Job Spooler'"
            print >>sys.stdout, "by@ Belal Salem, at 'Nothing Real VFX'"
            print >>sys.stdout, "www.nothing-real.com"

            if self.genMsgEnabled:
                Dismiss = 'Dismiss'
                message = QtGui.QMessageBox(self)
                message.setText('The Job Script was Generated Successfully.')
                message.setWindowTitle('Job Script...')
                message.setIcon(QtGui.QMessageBox.Information)
                message.addButton(Dismiss, QtGui.QMessageBox.AcceptRole)
                message.exec_()
                response = message.clickedButton().text()

        else:
            print >>sys.stderr, "OOOPs!!!! Somthing went wrong!!"
            print >>sys.stderr, "Couldn't generate the job script!"

    def sendAlfred(self):
        self.errorCheck()
        if not self.err:
            self.genMsgEnabled = False
            self.genTask()
            self.genMsgEnabled = True
            cmd = 'alfred ' + self.jobFullPath
            os.system(cmd)
            Dismiss = 'Dismiss'
            message = QtGui.QMessageBox(self)
            message.setText('The Job was sent to Alfred Successfully.')
            message.setWindowTitle('Job Script...')
            message.setIcon(QtGui.QMessageBox.Information)
            message.addButton(Dismiss, QtGui.QMessageBox.AcceptRole)
            message.exec_()
            response = message.clickedButton().text()

    def sendToTractor(self, internal=True):
        print >>sys.stderr, "Engine = {0}".format(self.engine)

        if internal:
            self.errorCheck()
            if not self.err:
                self.genMsgEnabled = False
                self.genTask()
                self.genMsgEnabled = True


                if self.standalone:
                    cmd = 'tractor-spool.py --engine=%s '%self.engine + '"%s"'%self.jobFullPath
                    print >>sys.stderr, cmd

                    os.system(cmd)
                else:
                    print >>sys.stderr, self.jobFullPath, self.priority

                    ####
                    from bs_pipeline.sync import find_scene_deps, submit_to_queue

                    (file_path, items) = find_scene_deps.gen()

                    items = [item.strip() for item in items]

                    deps = []
                    if items == ['']:
                        print >>sys.stderr, "Quitting, no item found to sync."
                        return

                    for item in items:
                        if ':' in item:
                            print >> sys.stderr, 'Please fix the dependencies inside this scene that are coming from a windows path.'
                            return

                        dep = item.replace('//', '/')
                        deps.append(dep)

                    clean_deps = list(set(deps))

                    item_list = []
                    for dep in clean_deps:
                        items = glob.glob(dep)
                        item_list.extend(items)

                    sync_list=''
                    for item in item_list:
                        sync_list += item + ' '

                    launch_type = None
                    # Based on the user action, we may have 3 different types of actions: 
                    # 1. Only Syncing of the assets => SYNC
                    # 2. Only render spool as the sync might have been previously done => RENDER
                    # 3. Both => SYNC_RENDER
                    if self.ui.checkBox.isChecked():
                        if self.ui.checkBox_2.isChecked():
                            launch_type='SYNC_RENDER'
                        else:
                            launch_type='SYNC'
                    elif self.ui.checkBox_2.isChecked():
                        launch_type='RENDER'
                    else:
                       self.dialog_box("Both `Sync` and `Render` can't be unchecked at the same time")
                       self.ui.checkBox.setChecked(True)
                       self.ui.checkBox_2.setChecked(True)

                    if launch_type is not None:
                        task_id = submit_to_queue.submit(launch_type=launch_type, alf_script=self.jobFullPath, dep_file=file_path, sync_list=sync_list, spool_dry_run=False)
                        self.dialog_box('Task ({0}) successfully submitted to the queue.'.format(task_id))
                    ####

                    # Send the task to the queue.
                    # The queue will take care of syncing of assets to the remote tractor and launch the render subsequently

                    #rfm.tractor.Spool(['--engine=%s'%self.engine, '--priority=%s'%str(self.priority), '%s'%self.jobFullPath])

        else: # running as a standalone function
            '''
            self.extraArgs = opt
            self.jobFullPath = tskScript
            self.task=seqInfo(tskFile, False)
            self.prjPath = prjPath
            self.tskStart = start
            self.taskEnd = end
            self.taskFile = tskFile
            '''
            print self.taskFile
            print self.tskStart
            print self.taskEnd
            if self.taskFile and self.tskStart and self.taskEnd:
                print 'Will generate the task and send to tractor'
                self.genTask(internal=False)
                rfm.tractor.Spool(['--engine=%s'%self.engine, '--priority=%s'%str(self.priority), '%s'%self.jobFullPath])


    def dialog_box(self, msg):
        self.genMsgEnabled = True
        Dismiss = 'Dismiss'
        message = QtGui.QMessageBox(self)
        message.setText(msg)
        message.setWindowTitle('Job Script...')
        message.setIcon(QtGui.QMessageBox.Information)
        message.addButton(Dismiss, QtGui.QMessageBox.AcceptRole)
        message.exec_()
        response = message.clickedButton().text()

    def renCp(self):
        '''
        Calls A python external exec file "seqRename" with the "-cp" option.
        '''
        fullPath = str(self.ui.qTaskSeq.text())
        os.system('seqRename -cp %s' %fullPath + self.tsr )

    def renMv(self):
        '''
        Calls A python external exec file "seqRename" with the '-mv' option.
        '''
        fullPath = str(self.ui.qTaskSeq.text())
        os.system('seqRename -mv %s' %fullPath + self.tsr)

    def render(self):
        prjDir = str(self.ui.qPrjPath.text())
        fullPath = str(self.ui.qTaskSeq.text())
        if self.renderCmd:
            os.system('cd ' + prjDir + '\n' + 'exec ' + self.renderCmd + fullPath + self.tsr)

def showSpooler(tskType = 0, imgPath=None, tskFile=False, prjPath=False, tskScript='', opt='', title='', start=False, end=False, priority=50, taskSize=1):
    tsT = tskType
    tsFile = tskFile
    pPath = prjPath
    tsSc = tskScript
    op = opt
    t = title
    p = priority
    st = start
    e = end
    pT = taskSize
    iP = imgPath
    try:
        if cmds.window(WINDOW_NAME, exists=True, q=True):
            cmds.deleteUI(WINDOW_NAME)
            dialog = None
        dialog = jobSpooler(imgPath=iP, tskType = tsT, tskFile=tsFile, prjPath=pPath, tskScript=tsSc, opt=op, title=t, start=st, end=e, priority=p, taskSize=pT, standalone=False)
        dialog.show()
        return
    except:
        app = QtGui.QApplication(sys.argv)
        myApp = jobSpooler(imgPath=iP, tskType = tsT, tskFile=tsFile, prjPath=pPath, tskScript=tsSc, opt=op, title=t, start=st, end=e, priority=p, taskSize=pT)
        myApp.show()
        sys.exit(app.exec_())
        return
