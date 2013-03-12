import sys
from PyQt4 import QtGui,QtCore


class Example(QtGui.QWidget):
    
    assets = 'assets/'
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initMenu(self): 
        newAction = QtGui.QAction(QtGui.QIcon(self.assets+'database_add.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New Connection')
        #newAction.triggered.connect(QtGui.qApp.quit)
        
        exitAction = QtGui.QAction(QtGui.QIcon(self.assets+'door_out.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(exitAction)
        
    def initTree(self):
        pass
    
    def initLayout(self):
        hbox = QtGui.QHBoxLayout(self)

        topleft = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
 
        topright = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)

        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
    def initUI(self):               
        self.initLayout()               
        #self.initMenu()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('SSQB')    
        self.show()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
