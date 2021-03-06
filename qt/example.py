import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.frame = QtGui.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(9, 9, 361, 291))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtGui.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(379, 9, 261, 291))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.lineEdit = QtGui.QLineEdit(self.frame_2)
        self.lineEdit.setGeometry(QtCore.QRect(92, 30, 161, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(10, 37, 70, 21))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(92, 63, 161, 28))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 70, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_3 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(92, 126, 161, 28))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(10, 133, 70, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(92, 93, 161, 28))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 70, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(90, 190, 161, 28))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtGui.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(8, 197, 70, 21))
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(90, 157, 161, 28))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_6 = QtGui.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(8, 164, 70, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtGui.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(8, 260, 70, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtGui.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(8, 227, 70, 21))
        self.label_8.setObjectName("label_8")
        self.lineEdit_7 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(90, 253, 161, 28))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtGui.QLineEdit(self.frame_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(90, 220, 161, 28))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.frame_3 = QtGui.QFrame(self)
        self.frame_3.setGeometry(QtCore.QRect(650, 10, 261, 291))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.plainTextEdit = QtGui.QPlainTextEdit(self.frame_3)
        self.plainTextEdit.setGeometry(QtCore.QRect(13, 11, 241, 231))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtGui.QPushButton(self.frame_3)
        self.pushButton.setGeometry(QtCore.QRect(10, 250, 120, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(self.frame_3)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 250, 101, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.setWindowTitle('Dialog')
        
        
        self.label.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8)) 
        
                
        self.show()        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
