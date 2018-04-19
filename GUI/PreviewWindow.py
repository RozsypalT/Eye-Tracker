from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_PreviewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

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
        self.closeButton.clicked.connect(lambda: self.close())
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

        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.nextButton, 1, 5, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.backButton, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def done(self):
        self.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Preview"))
        self.doneButton.setText(_translate("MainWindow", "Done"))
        self.closeButton.setText(_translate("MainWindow", "Close"))
        self.nextButton.setText(_translate("MainWindow", "Next"))
        self.backButton.setText(_translate("MainWindow", "Back"))

