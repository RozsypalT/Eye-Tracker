from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QLabel


class Ui_PreviewWindow(QMainWindow):
    def __init__(self, mainWin):
        super().__init__()
        self.setupUi(self)
        self.imageLabels = []
        self.firstIndex = 0
        self.secondIndex = 0
        self.mainWin = mainWin
        self.i = 0
        self.j = 0
        self.selected = []
        self.rows = 0
        self.cols = 0
        self.highlighted = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(651, 498)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.doneButton = QtWidgets.QPushButton(self.centralwidget)
        self.doneButton.setObjectName("pushButton_3")
        self.doneButton.clicked.connect(lambda: self.done())
        self.gridLayout.addWidget(self.doneButton, 1, 2, 1, 1)

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
        self.gallerygrid.setSpacing(20)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 6)

        self.switchButton = QtWidgets.QPushButton(self.centralwidget)
        self.switchButton.setObjectName("pushButton_2")
        self.switchButton.clicked.connect(self.switch)
        self.gridLayout.addWidget(self.switchButton, 1, 5, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def done(self):
        self.mainWin.updateSelected(self.selected)
        self.mainWin.show()
        self.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Preview"))
        self.doneButton.setText(_translate("MainWindow", "Done"))
        self.closeButton.setText(_translate("MainWindow", "Close"))
        self.switchButton.setText(_translate("MainWindow", "Switch"))

    def highlight(self, event, label):
        if len(self.highlighted) == 0:
            label.setStyleSheet("border: 5px inset red")
            self.highlighted.append(label)
        elif len(self.highlighted) == 1:
            if self.highlighted[0] == label:
                label.setStyleSheet("border: 5px inset white")
                self.highlighted.remove(label)
            else:
                label.setStyleSheet("border: 5px inset red")
                self.highlighted.append(label)
        elif len(self.highlighted) == 2:
            if self.highlighted[0] == label or self.highlighted[1] == label:
                label.setStyleSheet("border: 5px inset white")
                self.highlighted.remove(label)
            else:
                self.highlighted[0].setStyleSheet("border: 5px inset white")
                self.highlighted.pop(0)
                label.setStyleSheet("border: 5px inset red")
                self.highlighted.append(label)
        else:
            return


    def switch(self):
        self.i = 0
        self.j = 0

        if len(self.highlighted) < 2:
            return

        for i, lab in enumerate(self.imageLabels):
            if lab == self.highlighted[0]:
                self.firstIndex = i
            if lab == self.highlighted[1]:
                self.secondIndex = i

        for lab in self.imageLabels:
            lab.close()

        firstLab = self.imageLabels[self.firstIndex]
        secondLab = self.imageLabels[self.secondIndex]
        self.imageLabels[self.firstIndex] = secondLab
        self.imageLabels[self.secondIndex] = firstLab

        firstName = self.selected[self.firstIndex]
        secondName = self.selected[self.secondIndex]
        self.selected[self.firstIndex] = secondName
        self.selected[self.secondIndex] = firstName

        self.highlighted[0].setStyleSheet("border: 5px inset white")
        self.highlighted[1].setStyleSheet("border: 5px inset white")
        self.highlighted = []

        for lab in self.imageLabels:
            self.gallerygrid.addWidget(lab, self.i, self.j)
            lab.show()
            self.i = self.i + 1
            if self.i == self.rows:
                self.i = 0
                self.j = self.j + 1


    def organizeImages(self, filename):
            if filename == '':
                return
            label = QLabel(self.frame)
            pixmap = QPixmap(filename)
            label.setFixedSize(120, 120)
            modpixmap = pixmap.scaled(110, 110)
            label.setPixmap(modpixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: white")
            label.mousePressEvent = lambda event: self.highlight(event, label)
            self.imageLabels.append(label)
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

    def closeEvent(self, QCloseEvent):
        self.mainWin.show()
        self.close()