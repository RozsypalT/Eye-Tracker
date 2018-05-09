
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QMessageBox


from ResultsWindow import Ui_ResultsWindow


class Ui_ChooserWindow(QMainWindow):
    def __init__(self, mainWin):
        super().__init__()
        self.finished = False
        self.chosenImages = []
        self.mainWin = mainWin
        self.resWin = Ui_ResultsWindow(self.mainWin)
        self.setupUi(self)

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

        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.backButton, 1, 0, 1, 1)

        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.nextButton, 1, 5, 1, 1)

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

        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.backButton.setText(_translate("MainWindow", "Back"))
        self.nextButton.setText(_translate("MainWindow", "Next"))
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
