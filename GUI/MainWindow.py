
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ChooserWindow import Ui_ChooserWindow
from PreviewWindow import Ui_PreviewWindow

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title = 'Image Chooser'
        self.width = 1000
        self.height = 800
        self.selected = []
        screen = app.primaryScreen()
        self.height = 800
        size = screen.size()
        self.window_width = int(size.width() / 1.75)
        self.window_height = int((3.5 * size.height()) / 5)
        self.imgcountlabel = QLabel(self)
        self.comboboxlabel = QLabel(self)
        self.gallerylabel = QLabel(self)
        self.countlabel = QLabel(self)
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
        self.chooserWin = None
        self.previewWin = None
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(self.window_width, self.window_height)
        MainWindow.setWindowTitle(self.title)

        self.centralwidget.setObjectName("centralwidget")

        self.gallerylabel.setGeometry(
            QtCore.QRect(int(self.window_width / 4.5), int(0.5 * self.window_height / 15), int(self.window_width / 10),
                         int(self.window_height / 25)))
        self.gallerylabel.setText("Selected pictures:")

        self.imgcountlabel.setGeometry(
            QtCore.QRect(int(self.window_width / 4.5), int(12.4 * self.window_height / 15), int(self.window_width),
                         int(self.window_height / 25)))
        self.imgcountlabel.setText("Number of selected pictures: " + str(len(self.selected)) + ". " + str(
            self.x * self.y - len(self.selected)) + " more pictures needed.")

        self.comboboxlabel.setGeometry(
            QtCore.QRect(int(self.window_width / 15), int(2.5 * self.window_height / 15), int(self.window_width / 10),
                         int(self.window_height / 25)))
        self.comboboxlabel.setText("Layout:")

        self.addbutton.setText("Add Pictures")
        self.addbutton.setGeometry(QtCore.QRect(int(self.window_width/15), int(self.window_height/15), int(self.window_width/10), int(self.window_height/25)))
        self.addbutton.clicked.connect(self.addPictures)
        self.addbutton.setObjectName("pushButton")

        self.removebutton.setText("Remove")
        self.removebutton.setGeometry(QtCore.QRect(int(self.window_width/15), int(2*(self.window_height/15)), int(self.window_width/10), int(self.window_height/25)))
        self.removebutton.clicked.connect(self.removePicture)
        self.removebutton.setObjectName("pushButton_2")

        self.previewbutton.setText("Preview")
        self.previewbutton.setGeometry(QtCore.QRect(int(self.window_width/15), int(4*(self.window_height/15)), int(self.window_width/10), int(self.window_height/25)))
        self.previewbutton.clicked.connect(self.startPreviewProcess)
        self.previewbutton.setObjectName("pushButton_3")

        self.helpbutton.setText("Help")
        self.helpbutton.setGeometry(
            QtCore.QRect(int(self.window_width / 15), int(5 * (self.window_height / 15)), int(self.window_width / 10),
                         int(self.window_height / 25)))
        self.helpbutton.clicked.connect(self.startImageChooserProcess)
        self.helpbutton.setObjectName("pushButton_4")

        self.startbutton.setText("Start")
        self.startbutton.setGeometry(
            QtCore.QRect(int(self.window_width / 3), int(13.5 * (self.window_height / 15)), int(self.window_width / 10),
                         int(self.window_height / 25)))
        self.startbutton.clicked.connect(self.startImageChooserProcess)
        self.startbutton.setObjectName("pushButton_4")

        self.quitbutton.setText("Quit")
        self.quitbutton.setGeometry(QtCore.QRect(int(self.window_width / 1.75), int(13.5 * (self.window_height / 15)),
                                                 int(self.window_width / 10), int(self.window_height / 25)))
        self.quitbutton.clicked.connect(self.quit)
        self.quitbutton.setObjectName("pushButton_4")

        self.layoutbox.setGeometry(
            QtCore.QRect(int(self.window_width / 15), int(3 * self.window_height / 15), int(self.window_width / 10),
                         int(self.window_height / 25)))
        self.layoutbox.setObjectName("layout")
        self.layoutbox.addItem("3x3")
        self.layoutbox.addItem("3x2")
        self.layoutbox.addItem("2x3")
        self.layoutbox.addItem("2x2")
        self.layoutbox.currentTextChanged.connect(self.selection)

        self.gallery.setGeometry(
            QtCore.QRect(int(self.window_width / 4.5), int(self.window_height / 15), int((self.window_width / 1.75)),
                         int((self.window_height / 1.3))))
        self.gallery.setWidgetResizable(True)
        self.gallery.setWidgetResizable(True)

        self.gallery.setFixedWidth(int((self.window_width / 1.75)))
        self.gallery.setObjectName("gallery")
        self.gallery.setObjectName("gallery")




        self.gallerycontents.setGeometry(
            QtCore.QRect(0, 0, int((self.window_width / 1.75)), int((self.window_height / 1.3))))
        self.gallerycontents.setObjectName("scrollAreaWidgetContents")

        self.gallerygrid.setObjectName("gridLayout")

        self.gallery.setWidget(self.gallerycontents)

        MainWindow.setCentralWidget(self.centralwidget)


    def selection(self, value):
        str_res = value.split("x")
        self.x = int(str_res[0])
        self.y = int(str_res[1])
        self.imgcountlabel.setText("Number of selected pictures: " + str(len(self.selected)) + ". " + str(
            self.x * self.y - len(self.selected)) + " more pictures needed.")

    def addPictures(self):
        file = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileName()", "",
                                               "Image Files (*.png *.jpg)")
        print(file)
        for l in range(0, len(file[0])):

            filename = file[0][l]
            self.loadPicture(filename)

        self.imgcountlabel.setText("Number of selected pictures: " + str(len(self.selected)) + ". " + str(
            self.x * self.y - len(self.selected)) + " more pictures needed.")

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

        self.imgcountlabel.setText("Number of selected pictures: " + str(len(self.selected)) + ". " + str(
            self.x * self.y - len(self.selected)) + " more pictures needed.")

    def highlight(self, event, label):
        if self.highlighted is None:
            label.setStyleSheet("border: 5px inset red")
            self.highlighted = label
        elif self.highlighted == label:
            label.setStyleSheet("background-color: white")
            self.highlighted = None
        else:
            self.highlighted.setStyleSheet("background-color: white")
            self.highlighted = label
            label.setStyleSheet("border: 5px inset red")

    def loadPicture(self, filename):
        if filename == '':
            return
        self.selected.append(filename)
        label = QLabel(self.gallerycontents)
        pixmap = QPixmap(filename)
        label.setFixedSize(int((self.window_width / 1.75) / 3.25), int((self.window_height / 1.3) / 3.175))
        modpixmap = pixmap.scaled(int((self.window_width / 1.75) / 3.25) - 15,
                                  int((self.window_height / 1.3) / 3.175) - 15)
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
        self.chooserWin = Ui_ChooserWindow(self)
        self.chooserWin.showFullScreen()
        self.chooserWin.loadImages(self.selected, self.x, self.y)
        self.hide()

    def startPreviewProcess(self):
        self.hide()
        self.previewWin = Ui_PreviewWindow(self)
        self.previewWin.show()
        self.previewWin.loadImages(self.selected, self.x, self.y)

    def updateSelected(self, selected):
        self.selected = selected

def startApp():
        app = QtWidgets.QApplication(sys.argv)
        mainWin = Ui_MainWindow(app)
        mainWin.show()
        sys.exit(app.exec_())