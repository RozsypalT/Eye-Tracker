import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel

from ResultsWindow import Ui_ResultsWindow
from threading import Thread


class Ui_ChooserWindow(QMainWindow):
    def __init__(self, mainWin, plugin):
        super().__init__()
        self.plugin = plugin
        self.finished = False
        self.chosenImages = []
        self.mainWin = mainWin
        self.resWin = None
        self.i = 0
        self.j = 0
        self.selected = []
        self.rows = 0
        self.cols = 0
        self.highlighted = []
        self.setupUi(self)
        self.num = -1
        self.num2 = -1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.finishButton = QtWidgets.QPushButton(self.centralwidget)
        self.finishButton.setObjectName("pushButton_3")
        self.finishButton.clicked.connect(self.showResults)
        self.gridLayout.addWidget(self.finishButton, 1, 2, 1, 1)

        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("pushButton")
        self.closeButton.clicked.connect(self.close)
        self.gridLayout.addWidget(self.closeButton, 1, 3, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gallerygrid = QtWidgets.QGridLayout(self.frame)
        self.gallerygrid.setObjectName("gridLayout_2")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 6)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F:
            if self.windowState() & Qt.WindowFullScreen:
                self.showNormal()
            else:
                self.showFullScreen()

    def showResults(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Information)

        alert.setText("Finish the image choosing process!")
        alert.setInformativeText("Do you want to finish the process and show the results?")
        alert.setWindowTitle("Image Chooser")
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ans = alert.exec_()

        if ans == QMessageBox.Ok:
            self.finished = True
            self.resWin = Ui_ResultsWindow(self.mainWin)
            self.resWin.setChosenImages(self.chosenImages)
            self.resWin.show()
            self.close()

    def closeEvent(self, QCloseEvent):
        if not self.finished:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Information)

            alert.setText("Closing the image choosing window!")
            alert.setInformativeText("Do you really want to close this window?")
            alert.setWindowTitle("Image Chooser")
            alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            ans = alert.exec_()
            if ans == QMessageBox.Ok:
                self.mainWin.show()
                self.close()
            else:
                QCloseEvent.ignore()
        else:
            self.close()

    def organizeImages(self, filename):
        if filename == '':
            return
        label = QLabel(self.frame)
        pixmap = QPixmap(filename)
        label.setFixedSize(200, 200)
        modpixmap = pixmap.scaled(190, 190)
        label.setPixmap(modpixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background-color: white")
        # label.mousePressEvent = lambda event: self.highlight(event, label)
        # self.imageLabels.append(label)
        self.gallerygrid.addWidget(label, self.i, self.j)

        self.i = self.i + 1
        if self.i == self.rows:
            self.i = 0
            self.j = self.j + 1

    def loadImages(self, selected, rows, cols):
        self.rows = rows
        self.cols = cols
        self.selected = selected
        self.setupGrid()
        for filename in self.selected:
            self.organizeImages(filename)

    def setupGrid(self):
        for i in range(0, self.rows):
            self.gallerygrid.setRowStretch(i, 1)

        for i in range(0, self.cols):
            self.gallerygrid.setColumnStretch(i, 1)
        
    def setNums(self, num, num2):
        self.num = num
        self.num2 = num2
        print(self.num)
        print(self.num2)
        
        