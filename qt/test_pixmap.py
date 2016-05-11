#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we dispay an image
on the window. 

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout()
        pixmap = QtGui.QPixmap("/home/abhishek/Downloads/alert.png")

        lbl = QtGui.QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        
        btn1 = QtGui.QPushButton("foo")
        btn2 = QtGui.QPushButton("bar")
        
        hbox1 = QtGui.QHBoxLayout()
        
        """
        vbox1 = QtGui.QHBoxLayout()
        vbox2 = QtGui.QHBoxLayout()
        
        vbox1.addWidget(btn1)
        vbox2.addWidget(btn2)
        
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        """
        
        hbox1.addWidget(btn1)
        hbox1.addWidget(btn2)
               
        hbox.addLayout(hbox1)
        
        self.setLayout(hbox)
        
        self.setWindowTitle('Test Window')

        self.show()        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
