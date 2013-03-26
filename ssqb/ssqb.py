import os, sys, ConfigParser
from PyQt4 import QtGui,QtCore
from ui import Ui_MainWindow
import MySQLdb
from ssqb_db import SsqbDb
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class StartQt(QtGui.QMainWindow):
    conf = "conf.ini"
    assets = "assets/"
    activeDb = ""
    activeTable = ""
    type_id = 35
    to_check = ["delete","drop","truncate"]
    to_add_server = ["Name","Host","Username","Password"]
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initSlots()
        self.initMenu()
    def setStatus(self, text):
        self.statusBar().showMessage(text)
    def initSlots(self):
        self.statusBar()
        self.ui.clear_button.clicked.connect(self.clearAction)
        self.ui.new_button.clicked.connect(self.newAction)
        self.ui.query_button.clicked.connect(self.queryAction)
        self.ui.list.clicked.connect(self.listAction())
        self.ui.new_server.triggered.connect(self.addServer())
    def initMenu(self):
        self.config = ConfigParser.ConfigParser()
        # os.path.expanduser('~') + '/' + self.ssqb_dir + '/' + 
        self.ui.servers_menu.clear()
        self.config.read(self.conf)
        for name in self.config._sections:
            item = QtGui.QAction(QtGui.QIcon(self.assets+"database_connect.png"), name, self)
            item.triggered.connect(self.dbConnect(self.config._sections[name]["host"], self.config._sections[name]["user"], self.config._sections[name]["pass"]))
            self.ui.servers_menu.addAction(item);
    def progressBar(self):
        pass
    def queryAction(self):
        activeTab = self.ui.tab.currentWidget()
        queryField = activeTab.findChild(QtGui.QPlainTextEdit)
        sql = queryField.toPlainText()
        proceed = True
        danger = False
        for word in self.to_check:
            if word in sql.toLower():
                danger = True
                self.danger_word = word
                msg = "Are you sure you want to %s?" % word
                reply = QtGui.QMessageBox.question(self, 'Message', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.No:
                    proceed = False
                    break
        if not proceed:    
            pass
        else:
            self.progress = QtGui.QProgressDialog("Please Wait", "Cancel", 0, 100, self.ui.result_table)
            self.progress.setWindowModality(QtCore.Qt.WindowModal)
            self.progress.setAutoReset(True)
            self.progress.setAutoClose(True)
            self.progress.setMinimum(0)
            self.progress.setMaximum(100)
            self.progress.resize(800,220)
            self.progress.setWindowTitle("Running Query")
            self.progress.show()
            self.progress.setValue(0)
            self.progress.setValue(10)

            self.db.query(str(sql))
            self.progress.setValue(25)
            if danger:
                QtGui.QMessageBox.information(self,"Message","Item was %s" % self.danger_word)
            self.showResults()
    def showResults(self):
        
        fields = self.db.getFields()
        rows = self.db.getRows()
        self.progress.setValue(30)
        self.ui.result_table.clear()
        self.ui.result_table.setColumnCount(len(fields))
        self.ui.result_table.setRowCount(len(rows))
        header = self.ui.result_table.horizontalHeader()
        self.ui.result_table.setHorizontalHeaderLabels(fields)
        i = 1
        for row in rows:
            j = 0
            for v in row:
                item = QtGui.QTableWidgetItem(str(v))
                if i % 2:
                    item.setBackgroundColor(QtGui.QColor(221,221,221))
                self.ui.result_table.setItem(i,j,item)
                j += 1
            i += 1
        self.progress.setValue(100)    
        self.progress.hide()        
        header.setStretchLastSection(True)
        #header.setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.result_table.setVisible(False)
        self.ui.result_table.resizeColumnsToContents()
        self.ui.result_table.resizeRowsToContents()
        self.ui.result_table.setVisible(True)
    def clearAction(self):
        self.ui.query_field.clear()
    def newAction(self):
        next_id = self.ui.tab.count() + 1
        new_tab = QtGui.QWidget()
        new_tab.setObjectName(_fromUtf8("tab_%i" % next_id))
        new_query_field = QtGui.QPlainTextEdit(new_tab)
        new_query_field.setGeometry(QtCore.QRect(0, 0, 711, 161))
        new_query_field.setObjectName(_fromUtf8("query_field"))        
        vl = QtGui.QVBoxLayout(new_tab)
        vl.addWidget(new_query_field)
        self.ui.tab.addTab(new_tab, _fromUtf8("")) 
        self.ui.tab.setTabText(self.ui.tab.indexOf(new_tab), QtGui.QApplication.translate("MainWindow", "Tab %i" % next_id, None, QtGui.QApplication.UnicodeUTF8)) 
        self.ui.tab.setCurrentIndex(self.ui.tab.indexOf(new_tab))  
    def addServer(self):
        def callback():
            self.dialog = QtGui.QWidget()
            save = QtGui.QPushButton("Save")
            test = QtGui.QPushButton("Test")
            cancel = QtGui.QPushButton("Cancel")
            cancel.clicked.connect(self.clearForm())
            test.clicked.connect(self.testConnect())
            save.clicked.connect(self.saveServer())
            hbox = QtGui.QHBoxLayout()
            vbox = QtGui.QVBoxLayout()

            for field in self.to_add_server:
                item = QtGui.QLineEdit()
                item.setObjectName(field.lower())
                label = QtGui.QLabel(item)
                label.setText(field + ":")
                vbox.addWidget(label)
                vbox.addWidget(item)
            hbox.addStretch(1)
            hbox.addWidget(test)
            hbox.addWidget(save)
            hbox.addWidget(cancel)

            vbox.addStretch(1)
            vbox.addLayout(hbox)
            
            self.dialog.setLayout(vbox)
            self.dialog.move(QtGui.QApplication.desktop().screen().rect().center() - self.rect().center())            
            self.dialog.show()
        return callback
    def clearForm(self):
        def callback():
            sender = self.sender()
            widget = sender.parent()
            for a in widget.findChildren(QtGui.QLineEdit):
                a.clear()
            widget.close()
        return callback 
    def testConnect(self):
        def callback():
            sender = self.sender()
            widget = sender.parent()
            tmp = {}
            for a in widget.findChildren(QtGui.QLineEdit):
                tmp[str(a.objectName())] = str(a.text())
            try:
                con = MySQLdb.connect(tmp['host'], tmp['username'], tmp['password'])
                msg = "Connection successful, WOOT!"
            except:
                msg = "Awwww. Sorry, that info didn't work."
                pass
            QtGui.QMessageBox.information(self, "Connection Test to %s" % tmp['host'], msg)
        return callback
    def saveServer(self):
        def callback():
            sender = self.sender()
            widget = sender.parent()
            tmp = {}
            for a in widget.findChildren(QtGui.QLineEdit):
                tmp[str(a.objectName())] = str(a.text())
            self.config.add_section(tmp["name"])
            self.config.set(tmp["name"], "host", tmp["host"])
            self.config.set(tmp["name"], "user", tmp["username"])
            self.config.set(tmp["name"], "pass", tmp["password"])
            with open(self.conf, 'wb') as configfile:
                self.config.write(configfile)            
            for a in widget.findChildren(QtGui.QLineEdit):
                a.clear()
            widget.close()
            self.initMenu()
            QtGui.QMessageBox.information(self, "Message", "Connection Saved!")
        return callback
    def dbConnect(self, host, user, passwrd):
        def callback():
            self.db = SsqbDb(host,user,passwrd)
            databases = self.db.getDbs()
            self.ui.list.clear()
            for db in databases:
                item = QtGui.QListWidgetItem(db['Database'])
                item.setData(self.type_id, "db")
                self.ui.list.addItem(item)
        return callback
    def listAction(self):
        def callback():
            sender = self.sender()
            item = sender.currentItem()
            item_type = item.data(self.type_id)
            if item_type == "db":
                rtn = self.dbUseDb()
            elif item_type == "table":
                rtn = self.dbUseTable()
        return callback
    def dbUseDb(self):
        sender = self.sender()
        self.activeDb = item = sender.currentItem().text()
        query = "USE %s" % item
        self.db.queryNoVals(query)
        self.setStatus("%s is now the active database" % item)
        tables = self.db.getTables(item)
        self.ui.list.clear()
        for table in tables:
            item = QtGui.QListWidgetItem(table[0])
            item.setData(self.type_id, "table")
            self.ui.list.addItem(item)
    def dbUseTable(self):
        sender = self.sender()
        self.activeTable = item = sender.currentItem().text()
        query = "SELECT * FROM %s LIMIT 1000" % item
        self.setStatus("%s is now the active table" % item)
        self.activeTab = self.ui.tab.currentWidget()
        self.activeQueryField = self.activeTab.findChild(QtGui.QPlainTextEdit)
        self.activeQueryField.setPlainText(query)
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = StartQt()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
