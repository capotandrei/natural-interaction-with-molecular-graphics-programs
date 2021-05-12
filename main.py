from PyQt5 import QtWidgets
import sys
from gui import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    ui = Ui_window()
    ui.setupUi(window)
    ui.set_buttons()
    window.show()
    sys.exit(app.exec_())