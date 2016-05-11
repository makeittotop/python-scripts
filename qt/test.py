import sys
from PyQt4 import QtCore, QtGui

from scrollable_widget import Ui_Dialog  
from widget_proto2 import Ui_Form
from test_form import Ui_Form
 
class MyTestClass(QtGui.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent)
        #self.ui = Ui_Dialog()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
 
app = QtGui.QApplication(sys.argv)
myWindow = MyTestClass(None)
myWindow.show()
app.exec_()
