import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel
from ResultsWindow import Ui_ResultsWindow
from threading import Thread
from time import *

# defines image choosing window
class Ui_ChooserWindow(QMainWindow):
    def __init__(self, mainWin):
        super().__init__()
        self.window_width = mainWin.window_width
        self.window_height = mainWin.window_height
        self.finished = False
        self.chosenImage = None
        self.mainWin = mainWin
        self.resWin = None
        self.i = 0
        self.j = 0
        self.selected = []
        self.rows = 0
        self.cols = 0
        self.highlighted = None
        self.labellist = []
        self.setupUi(self)
        self.time = 0
        self.started = True

    # initializes UI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        MainWindow.setWindowIcon(QtGui.QIcon("icon.png"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.finishButton = QtWidgets.QPushButton(self.centralwidget)
        self.finishButton.setObjectName("pushButton_3")
        self.finishButton.clicked.connect(self.showResults)
        self.gridLayout.addWidget(self.finishButton, 3, 0, 1, 1)

        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("pushButton")
        self.closeButton.clicked.connect(self.close)
        self.gridLayout.addWidget(self.closeButton, 4, 0, 1, 1)
        
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gallerygrid = QtWidgets.QGridLayout(self.frame)
        self.gallerygrid.setObjectName("gridLayout_2")
        self.gridLayout.addWidget(self.frame, 1, 1, 6, 1)
        
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 10)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Chooser"))
        self.finishButton.setText(_translate("MainWindow", "Finish"))
        self.closeButton.setText(_translate("MainWindow", "Close"))

    # changes window from fullscreen mode to windowed mode if "F" key is pressed
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F:
            if self.windowState() & Qt.WindowFullScreen:
                self.showNormal()
            else:
                self.showFullScreen()

    # displays new window with selected pictures
    def showResults(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Information)
        alert.setWindowIcon(QtGui.QIcon("icon.png"))

        alert.setText("Finish the image choosing process!")
        alert.setInformativeText("Do you want to finish the process and show the results?")
        alert.setWindowTitle("Image Chooser")
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ans = alert.exec_()

        if ans == QMessageBox.Ok:
            self.finished = True
            self.resWin = Ui_ResultsWindow(self.mainWin)
            self.resWin.loadImages(self.chosenImage)
            self.resWin.show()
            self.close()

    # displays confirmation window when user closes the image choosing window, show main window upon exit
    def closeEvent(self, QCloseEvent):
        if not self.finished:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Information)
            alert.setWindowIcon(QtGui.QIcon("icon.png"))

            alert.setText("Closing the image choosing window!")
            alert.setInformativeText("Do you really want to close this window?")
            alert.setWindowTitle("Image Chooser")
            alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            ans = alert.exec_()
            if ans == QMessageBox.Ok:
                self.mainWin.show()
                self.close()
                self.started = False
            else:
                QCloseEvent.ignore()
        else:
            self.close()
            self.started = False

    # organizes images into grid in chooser window
    def organizeImages(self, filename):
        if filename == '':
            return
        label = QLabel(self.frame)
        pixmap = QPixmap(filename)
        label.setFixedSize(int(self.window_width/self.cols), int(self.window_height/self.rows))
        modpixmap = pixmap.scaled(int(self.window_width/self.cols)-20, int(self.window_height/self.rows)-20)
        label.setPixmap(modpixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background-color: white")
        self.labellist.append(label)
        self.gallerygrid.addWidget(label, self.i, self.j)

        self.i = self.i + 1
        if self.i == self.rows:
            self.i = 0
            self.j = self.j + 1

    # loads image data from main window
    def loadImages(self, selected, rows, cols):
        self.rows = rows
        self.cols = cols
        self.selected = selected
        self.setupGrid()
        for filename in self.selected:
            self.organizeImages(filename)

    # initializes grid layout
    def setupGrid(self):
        for i in range(0, self.rows):
            self.gallerygrid.setRowStretch(i, 1)

        for i in range(0, self.cols):
            self.gallerygrid.setColumnStretch(i, 1)

    # highlights selected pictures
    def highlight(self, i, j):
        #print(i)
        #print(j)
        
        if self.started is not True:
            return
        
        if self.time == 0:
            self.time = time()
        elif time() - self.time < 0.5:
            return
        else:
            self.time = time()
            
        if self.highlighted is None:
            self.labellist[i * self.cols + j].setStyleSheet("border: 5px inset red")
            self.highlighted = self.labellist[i * self.cols + j]
            self.chosenImage = self.selected[i * self.cols + j]
        elif self.highlighted == self.labellist[i * self.cols + j]:
            self.labellist[i * self.cols + j].setStyleSheet("background-color: white")
            self.highlighted = None
            self.chosenImage = None
        else:
            self.highlighted.setStyleSheet("background-color: white")
            self.highlighted = self.labellist[i * self.cols + j]
            self.labellist[i * self.cols + j].setStyleSheet("border: 5px inset red")
            self.chosenImage = self.selected[i * self.cols + j]

    # returns number of rows
    def getRows(self):
        return self.rows

    # returns number of columns
    def getCols(self):
        return self.cols
        
    def setStarted(self):
        self.started = True    