# Imports 
import sys
import platform

# from PySide2 import QtCore, QtGui, QtWidgets
# from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime,QUrl, Qt, QEvent)
# from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
# from PySide2.QtWidgets import *

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QPropertyAnimation

# Link GUI file
from design import Ui_MainWindow

# Import functions
from ui_functions import *
from api_functions import *

# Defines

# Functions

# Classes
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # super().__init__()

        # Toggle burger menu
        self.ui.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        # Show main window
        self.show()

# Launch
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    window = MainWindow()

    # API initialize
    # api = API.__init__()

    sys.exit(app.exec_())