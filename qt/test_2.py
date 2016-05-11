import sys
from PyQt4 import QtCore, QtGui

from scrollable_widget_2 import Ui_Dialog 
 
class MyTestClass(QtGui.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
 
app = QtGui.QApplication(sys.argv)
myWindow = MyTestClass(None)
myWindow.show()
app.exec_()
