
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ChooserWindow import Ui_ChooserWindow
from PreviewWindow import Ui_PreviewWindow

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Chooser'
        self.width = 1000
        self.height = 800
        self.selected = []
        self.imgcountlabel = QLabel(self)
        self.comboboxlabel = QLabel(self)
        self.centralwidget = QtWidgets.QWidget(self)
        self.addbutton = QtWidgets.QPushButton(self.centralwidget)
        self.removebutton = QtWidgets.QPushButton(self.centralwidget)
        self.previewbutton = QtWidgets.QPushButton(self.centralwidget)
        self.helpbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startbutton = QtWidgets.QPushButton(self.centralwidget)
        self.quitbutton = QtWidgets.QPushButton(self.centralwidget)
        self.layoutbox = QtWidgets.QComboBox(self.centralwidget)
        self.gallery = QtWidgets.QScrollArea(self.centralwidget)
        self.gallerycontents = QtWidgets.QWidget()
        self.gallerygrid = QtWidgets.QGridLayout(self.gallerycontents)
        self.gallerygrid.setColumnStretch(0, 10)
        self.gallerygrid.setColumnStretch(1, 10)
        self.gallerygrid.setColumnStretch(2, 10)
        self.gallerygrid.setRowStretch(0, 10)
        self.gallerygrid.setRowStretch(1, 10)
        self.gallerygrid.setRowStretch(2, 10)
        self.labellist = []
        self.testlabel = QLabel(self)
        self.highlighted = None
        self.i = 0
        self.j = 0
        self.x = 3
        self.y = 3
        self.chooserWin = Ui_ChooserWindow(self)
        self.previewWin = Ui_PreviewWindow(self)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
       # MainWindow.setFixedSize(1000, 800)

        self.centralwidget.setObjectName("centralwidget")

        self.comboboxlabel.setGeometry(QtCore.QRect(50,150,100,32))
        self.comboboxlabel.setText("Layout:")

        self.addbutton.setText("Add Pictures")
        self.addbutton.setGeometry(QtCore.QRect(50, 50, 100, 32))
        self.addbutton.clicked.connect(self.addPictures)
        self.addbutton.setObjectName("pushButton")

        self.removebutton.setText("Remove")
        self.removebutton.setGeometry(QtCore.QRect(50, 114, 100, 32))
        self.removebutton.clicked.connect(self.removePicture)
        self.removebutton.setObjectName("pushButton_2")

        self.previewbutton.setText("Preview")
        self.previewbutton.setGeometry(QtCore.QRect(50, 242, 100, 32))
        self.previewbutton.clicked.connect(self.startPreviewProcess)
        self.previewbutton.setObjectName("pushButton_3")

        self.helpbutton.setText("Help")
        self.helpbutton.setGeometry(QtCore.QRect(50, 308, 100, 32))
        self.helpbutton.clicked.connect(self.startImageChooserProcess)
        self.helpbutton.setObjectName("pushButton_4")

        self.startbutton.setText("Start")
        self.startbutton.setGeometry(QtCore.QRect(375, self.height-82, 100, 32))
        self.startbutton.setObjectName("pushButton_4")

        self.quitbutton.setText("Quit")
        self.quitbutton.setGeometry(QtCore.QRect(525, self.height-82, 100, 32))
        self.quitbutton.clicked.connect(self.quit)
        self.quitbutton.setObjectName("pushButton_4")

        self.layoutbox.setGeometry(QtCore.QRect(50, 178, 100, 32))
        self.layoutbox.setObjectName("layout")
        self.layoutbox.addItem("3x3")
        self.layoutbox.addItem("3x2")
        self.layoutbox.addItem("2x3")
        self.layoutbox.addItem("2x2")
        self.layoutbox.currentTextChanged.connect(self.selection)

        self.gallery.setGeometry(QtCore.QRect(187, 47, 603, 621))
        self.gallery.setWidgetResizable(True)
        self.gallery.setFixedWidth(620)
        self.gallery.setObjectName("gallery")

        self.gallerycontents.setGeometry(QtCore.QRect(0, 0, 620, 618))
        self.gallerycontents.setObjectName("scrollAreaWidgetContents")

        self.gallerygrid.setObjectName("gridLayout")

        self.gallery.setWidget(self.gallerycontents)

        MainWindow.setCentralWidget(self.centralwidget)


    def selection(self, value):
        str_res = value.split("x")
        self.x = int(str_res[0])
        self.y = int(str_res[1])

    def addPictures(self):
        file = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileName()", "",
                                               "Image Files (*.png *.jpg)")
        print(file)
        for l in range(0, len(file[0])):

            filename = file[0][l]
            self.loadPicture(filename)

    def removePicture(self):
        k = 0
        l = 0
        index = 0
        if self.highlighted is None:
            return
        else:
            for i, lab in enumerate(self.labellist):
                if lab == self.highlighted:
                    index = i
                    break
        self.selected.pop(index)
        for lab in self.labellist:
            lab.close()
        self.labellist.remove(self.highlighted)
        self.highlighted = None
        for lab in self.labellist:
            self.gallerygrid.addWidget(lab, l, k)
            k = k + 1
            if k == 3:
                l = l + 1
                k = 0
            lab.show()
        self.i = k
        self.j = l

    def highlight(self, event, label):
        if self.highlighted is None:
            label.setStyleSheet("border: 5px inset red")
            self.highlighted = label
        elif self.highlighted == label:
            label.setStyleSheet("border: 5px inset white")
            self.highlighted = None
        else:
            self.highlighted.setStyleSheet("border: 5px inset white")
            self.highlighted = label
            label.setStyleSheet("border: 5px inset red")

    def loadPicture(self, filename):
        if filename == '':
            return
        self.selected.append(filename)
        label = QLabel(self.gallerycontents)
        pixmap = QPixmap(filename)
        label.setFixedSize(190, 190)
        modpixmap = pixmap.scaled(180, 180)
        label.setPixmap(modpixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background-color: white")
        label.mousePressEvent = lambda event: self.highlight(event, label)
        self.labellist.append(label)
        self.gallerygrid.addWidget(label, self.j, self.i)
        self.i = self.i + 1

        if self.i == 3:
            self.i = 0
            self.j = self.j + 1

    def quit(self):
        self.close()

    def startImageChooserProcess(self):
        self.chooserWin.show()
        self.hide()

    def startPreviewProcess(self):
        self.hide()
        self.previewWin.show()
        self.previewWin.loadImages(self.selected, self.x, self.y)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Ui_MainWindow()
    mainWin.show()
    sys.exit(app.exec_())