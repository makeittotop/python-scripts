#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, datetime, getpass, csv, time
from pymongo import MongoClient, Connection

import shot_time_tracker


mongodb_uri = "mongodb://172.16.15.246:20000/"

class TimeTracker(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = shot_time_tracker.Ui_MainWindow()

        self.ui.setupUi(self)
        self.ui.frame.setStyleSheet(
                """QFrame { background-color: red; color: black }""")

        self.setFixedSize(400, 250)
        # enable custom window hint
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        # disable (but not hide) close button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.ui.start_button.clicked.connect(self.tt_action);

        self.client = MongoClient(mongodb_uri)
        self.conn = Connection(mongodb_uri)
        self.db = self.conn['time_tracker']

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  

    def tt_action(self):
        process_text = self.ui.process_editline.text()
        asset_text = self.ui.asset_editline.text()

        if process_text == '':
            self.showdialog("Process field can't be empty")
            #self.ui.process_editline.setStyleSheet(
                #"""QLineEdit { background-color: red; color: black }""")

        if asset_text == '':
            self.showdialog("Asset field can't be empty")
            #self.ui.asset_editline.setStyleSheet(
                #"""QLineEdit { background-color: red; color: black }""")

        process_text = process_text.replace(" ", "_")
        asset_text = asset_text.replace(" ", "_")
        user = getpass.getuser()

        if str(self.ui.start_button.text()).lower() == 'start':
            self.ui.process_editline.setEnabled(False)
            self.ui.asset_editline.setEnabled(False)

            self.ui.action_status_label.setText("Running")
            self.ui.start_button.setText("Stop")
            self.ui.frame.setStyleSheet(
                """QFrame { background-color: green; color: black }""")

            #db ops
            coll = self.db[user]
            doc_name = "{0}_{1}".format(process_text, asset_text)
            if coll.find({"name": doc_name}).count():
                cursor = coll.find({"name": doc_name})
                post=cursor[0]
                post['current_counter'] +=1
            else:    
                post = {
                  "name": doc_name,
                  "current_counter": 1
                }

            #start = 'start_{0}'.format(post['current_counter'])
            #date = 'date_start_{0}'.format(post['current_counter'])
            #start_seconds = 'start_seconds_{0}'.format(post['current_counter'])

            current_counter = "'{0}'".format(post['current_counter'])
            post[current_counter]={}
            post[current_counter]['start'] = time.strftime("%H:%M:%S")
            post[current_counter]['date_start'] = time.strftime("%d/%m/%Y")
            post[current_counter]['start_seconds'] = time.time()

            coll.update({"name": doc_name}, {"$set": post}, upsert=True)
            #coll.insert(post)

        elif str(self.ui.start_button.text()).lower() == 'stop':
            self.ui.process_editline.setEnabled(True)
            self.ui.asset_editline.setEnabled(True)

            self.ui.action_status_label.setText("Not Running")
            self.ui.start_button.setText("Start")
            self.ui.frame.setStyleSheet(
                """QFrame { background-color: red; color: black }""")

            #db ops
            coll = self.db[user]
            doc_name = "{0}_{1}".format(process_text, asset_text)

            if coll.find({"name": doc_name}).count():
                cursor = coll.find({"name": doc_name})
                post=cursor[0]
                
                #end = 'end_{0}'.format(post['current_counter'])
                #date = 'date_end_{0}'.format(post['current_counter'])
                #start_seconds = 'start_seconds_{0}'.format(post['current_counter'])
                #end_seconds = 'end_seconds_{0}'.format(post['current_counter'])
                #duration = 'duration_{0}'.format(post['current_counter'])
                current_counter = "'{0}'".format(post['current_counter'])
                post[current_counter]['end'] = time.strftime("%H:%M:%S")
                post[current_counter]['date_end'] = time.strftime("%d/%m/%Y")
                post[current_counter]['end_seconds'] = time.time()
                # minutes
                post[current_counter]['duration'] = (post[current_counter]['end_seconds'] - post[current_counter]['start_seconds']) / (60)

                coll.update({"name": doc_name}, {"$set": post}, upsert=False)

                # File Ops
                filename = "{0}_{1}.csv".format(process_text, asset_text)
                filecreation(user, filename, post)


    def showdialog(self, message):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)

       msg.setText(message)
       msg.setWindowTitle("Alert")
       #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       msg.setStandardButtons(QMessageBox.Ok)
       msg.buttonClicked.connect(self.msgbtn)
    
       retval = msg.exec_()
       print "value of pressed message box button:", retval

    def msgbtn(self, i):
       print "Button pressed is:",i.text()

    def myExitHandler(self):
        process_text = self.ui.process_editline.text()
        asset_text = self.ui.asset_editline.text()

        if process_text == '':
            self.showdialog("Process field can't be empty")
            #self.ui.process_editline.setStyleSheet(
                #"""QLineEdit { background-color: red; color: black }""")

        if asset_text == '':
            self.showdialog("Asset field can't be empty")
            #self.ui.asset_editline.setStyleSheet(
                #"""QLineEdit { background-color: red; color: black }""")

        process_text = process_text.replace(" ", "_")
        asset_text = asset_text.replace(" ", "_")
        user = getpass.getuser()

        if str(self.ui.start_button.text()).lower() == 'stop':
            #db ops
            coll = self.db[user]
            doc_name = "{0}_{1}".format(process_text, asset_text)

            if coll.find({"name": doc_name}).count():
                cursor = coll.find({"name": doc_name})
                post=cursor[0]
                
                current_counter = "'{0}'".format(post['current_counter'])
                post[current_counter]['end'] = time.strftime("%H:%M:%S")
                post[current_counter]['date_end'] = time.strftime("%d/%m/%Y")
                post[current_counter]['end_seconds'] = time.time()
                # minutes
                post[current_counter]['duration'] = (post[current_counter]['end_seconds'] - post[current_counter]['start_seconds']) / (60)

                coll.update({"name": doc_name}, {"$set": post}, upsert=False)

                # File Ops
                filename = "{0}_{1}.csv".format(process_text, asset_text)
                filecreation(user, filename, post)

        print("tada!")

def filecreation(user, filename, post):
    #mydir = os.path.join("/nas/sandbox/timetrack_app/data/{0}/".format(user), datetime.datetime.now().strftime('%Y-%m-%d'))
    mydir = "/nas/sandbox/timetrack_app/data/{0}/".format(user)

    #print(post)

    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error..
    with open(os.path.join(mydir, filename), 'wt') as f:
        try:
            writer = csv.writer(f)
            writer.writerow( ('Start Date', 'Start', 'End Date', 'End', 'Duration', 'Total') )
            counter = post.get('current_counter')
            total = 0
            for i in range(counter):
                _key = "'{0}'".format(i+1)
                total += post[_key]['duration']
                #writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
                writer.writerow( (post[_key]['date_start'], post[_key]['start'], post[_key]['date_end'], post[_key]['end'], post[_key]['duration'], total) )
        finally:
            pass

        print("Data written successfully.")  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tt_app = TimeTracker()
    app.aboutToQuit.connect(tt_app.myExitHandler)

    tt_app.show()
    sys.exit(app.exec_())
