#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui


class FileDialogClass(QtGui.QMainWindow):
    
    def __init__(self):
        super(FileDialogClass, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Save location ...', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Save location')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Save data dialog')
        self.show()
        
    def showDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Save data at ...', 
                '/home/abhishek')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data) 
                                
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = FileDialogClass()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()