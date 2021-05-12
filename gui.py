from PyQt5 import QtCore, QtGui, QtWidgets
import multiprocessing
from multiprocessing import Queue
from hand_gestures import HandGestures
from pymol_class import PymolRun
from head_tracking import BodyGameRuntime


class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(510, 366)
        self.zoom_button = QtWidgets.QPushButton(window)
        self.zoom_button.setGeometry(QtCore.QRect(60, 210, 91, 21))
        self.zoom_button.setObjectName("pushButton")
        self.fingers_button = QtWidgets.QPushButton(window)
        self.fingers_button.setGeometry(QtCore.QRect(200, 210, 121, 21))
        self.fingers_button.setObjectName("pushButton_2")
        self.headtracking_button = QtWidgets.QPushButton(window)
        self.headtracking_button.setGeometry(QtCore.QRect(360, 210, 91, 21))
        self.headtracking_button.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(window)
        self.label.setGeometry(QtCore.QRect(30, 60, 461, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(window)
        self.label_2.setGeometry(QtCore.QRect(-10, 0, 521, 371))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.label_2.setPalette(palette)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("background_img.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.cancel_button = QtWidgets.QPushButton(window)
        self.cancel_button.setGeometry(QtCore.QRect(300, 280, 91, 21))
        self.cancel_button.setObjectName("pushButton_4")
        self.pymol_button = QtWidgets.QPushButton(window)
        self.pymol_button.setGeometry(QtCore.QRect(130, 280, 91, 21))
        self.pymol_button.setObjectName("pushButton_5")
        self.label_2.raise_()
        self.zoom_button.raise_()
        self.fingers_button.raise_()
        self.headtracking_button.raise_()
        self.label.raise_()
        self.cancel_button.raise_()
        self.pymol_button.raise_()

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "GUI"))
        self.zoom_button.setText(_translate("window", "Zoom IN/OUT"))
        self.fingers_button.setText(_translate("window", "Fingers Commands"))
        self.headtracking_button.setText(_translate("window", "Head Tracking"))
        self.label.setText(_translate("window",
                                      "<font color = white>Natural interaction with molecular graphics programs"))
        self.cancel_button.setText(_translate("window", "Cancel"))
        self.pymol_button.setText(_translate("window", "Lauch PyMol"))

    def set_buttons(self):
        self.pymol_button.clicked.connect(run_pymol_thread)
        self.zoom_button.clicked.connect(zoom_thread)
        self.fingers_button.clicked.connect(fingers_thread)
        self.headtracking_button.clicked.connect(head_thread)
        self.cancel_button.clicked.connect(kill_process)


hg = HandGestures()
bg = BodyGameRuntime()
queue = Queue()
process_actual = None

def run_pymol_thread():
    process = multiprocessing.Process(target=PymolRun.main, args=(queue,))
    process.start()

def zoom_thread():
    global process_actual
    print('Zoom Thread')
    process = multiprocessing.Process(target=hg.zoom_controller, args=(queue,))
    process_actual = process
    process.start()

def fingers_thread():
    global process_actual
    print('Fingers count Thread')
    process = multiprocessing.Process(target=hg.fingers_count, args=(queue,))
    process_actual = process
    process.start()

def body_game(queue):
    global bg
    bg.run(queue)

def head_thread():
    global process_actual
    print('Head Tracking Thread')
    process = multiprocessing.Process(target=body_game, args=(queue,))
    process_actual = process
    process.start()

def kill_process():
    global process_actual
    print('TERMINATE')
    process_actual.terminate()




