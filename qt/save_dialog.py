#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import re
import requests

class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.pyqtSignal(object, object, object)

    def __init__(self, url, dname, count):
        QtCore.QThread.__init__(self)
        self.url = url
        self.dname = dname
        self.count = count

    def run(self):
        print self.count, self.url
        fname=self.url.split("/")[-1]
        save_fname = self.dname + '/' + fname
        print save_fname

        #self.data_downloaded.emit('%d - %s %s' % (self.count, "Downloading to", save_fname), 0)
        
        try:
            response = requests.get(self.url, stream=True)

            if response.ok:
                with open(save_fname, "wb") as handle:
                    for data in response.iter_content(chunk_size=5*1024):
                        handle.write(data)

                self.data_downloaded.emit(self.count, 1, save_fname)
            else:
               self.data_downloaded.emit(self.count, 2, self.url)
        except:
            e = sys.exc_info()[0]
            print e            
            self.data_downloaded.emit(self.count, 2, self.url)


class FileDialogClass(QtGui.QMainWindow):
    data=''
    progress=''
    status_list = []
     
    def __init__(self):
        super(FileDialogClass, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        downloadFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Download', self)
        downloadFile.setShortcut('Ctrl+D')
        downloadFile.setStatusTip('Download data')
        downloadFile.triggered.connect(self.showDownloadDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       
        downloadMenu = menubar.addMenu('&Download')
        downloadMenu.addAction(downloadFile)       
        
        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('File dialog')
        self.show()
        
    def showDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/tmp')
        
        f = open(fname, 'r')
        
        with f:        
            self.data = f.read()
            self.textEdit.setText(self.data) 
                                
        
    def updateText(self, message):
        self.textEdit.append(message)
            
    def showDownloadDialog(self):
        dname = QtGui.QFileDialog.getExistingDirectory(self, 'Save data at ...', 
                '/home/abhishek', QtGui.QFileDialog.ShowDirsOnly|QtGui.QFileDialog.DontResolveSymlinks)
        
        print dname

        url_list = self.data.split()
        self.threads = []
        count = 0

        self.status_list = ["Downloading: {0}\n".format(url) for url in url_list]
        self.textEdit.clear()
        
        for status in self.status_list:
            self.textEdit.insertPlainText(status) 

        for url in url_list:
            print url

            downloader = DownloadThread(url, dname, count)
            downloader.data_downloaded.connect(self.on_data_ready_2)
            self.threads.append(downloader)
            count += 1
            downloader.start()
            
    def on_data_ready_2(self, count, type, fname, error="ERROR"):
        if type == 1:
          self.status_list[count] = QtCore.QString("<font color=\"green\">Download complete: %1</font><br>").arg(fname)
          #self.status_list[count] = "Download complete: {0}\n".format(fname)
        elif type == 2:
          self.status_list[count] = QtCore.QString("<font color=\"red\">%1: %2</font><br>").arg(error, fname)
          #self.status_list[count] = "{0}: {1}\n".format(error, fname)

        self.textEdit.clear()
        
        for status in self.status_list:
            if re.search('complete:|error', status, re.IGNORECASE):
                self.textEdit.insertHtml(status)
            else:
               self.textEdit.insertPlainText(status)

    def on_data_ready(self, d, t):
        print d

        col = None
        if t:
            col = QtGui.QColor("red")
        else:
            col = QtGui.QColor("green")

        textColor = self.textEdit.textColor()
        self.textEdit.setTextColor(col)
        self.updateText(unicode(d))

        self.textEdit.setTextColor(textColor)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = FileDialogClass()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
