import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import custom widget
#from test_burning_widget import BurningWidget
#from test_pixmap import Example
#from example import Example
#from widget_proto2 import Ui_Form
#from scrollable_widget import Ui_Dialog
from test_form import Ui_Form

class Example(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        QWidget.__init__(self, parent)
        #self.ui = Ui_Dialog()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
class Widget(QWidget):

    def __init__(self, parent= None):
        super(Widget, self).__init__()

        
        # Add a button and connect it to its slot
        btn_new = QPushButton("Add new custom widget")
        self.connect(btn_new, SIGNAL('clicked()'), self.add_new_custom_widget)

        # the main widget
        self.widget = QWidget()
        # Add a vertical layout
        layout = QVBoxLayout(self)
        # Add a text line and disable it
        for _ in range(1):
            #c_w = BurningWidget()
            #c_w = Example()
            c_w = Example()
            layout.addWidget(c_w)
            
            #line_text = QLineEdit("foo")
            #line_text.setEnabled(False)
            # Add the text to the vertical widget
            #layout.addWidget(line_text)
            # Stretch it a little
            layout.addStretch()
        # Add the layout to the widget    
        self.widget.setLayout(layout)

        # Declare a QSrollArea and add the widget to it.
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Make it resizable
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        # The main window vertical layout 
        vLayout = QVBoxLayout(self)
        # Add a button to it
        vLayout.addWidget(btn_new)
        # Add scroll to it
        vLayout.addWidget(scroll)
        # Set this as the main widget layout
        self.setLayout(vLayout)

    def add_new_custom_widget(self):
        #line_text = QLineEdit("bar")
        c_w = Example()
        
        #c_w = MyWin().show()
        self.widget.layout().insertWidget(self.widget.layout().count() - 1, c_w)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dialog = Widget()
    dialog.show()

    app.exec_()
