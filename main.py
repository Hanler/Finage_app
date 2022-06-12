# Imports 
from operator import countOf
import sys
import platform
from traceback import print_tb

# from PySide2 import QtCore, QtGui, QtWidgets
# from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime,QUrl, Qt, QEvent)
# from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
# from PySide2.QtWidgets import *

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtCore import QPropertyAnimation

import requests
from datetime import datetime

# Link GUI file
from design import Ui_MainWindow

# Import functions
from ui_functions import *

# Defines

# Functions

# Classes

class MainWindow(QMainWindow):
    def __init__(self):
        # QMainWindow.__init__(self)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # super().__init__()

        # Toggle burger menu
        self.ui.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        # API initialize
        api = API(self)

        # Show main window
        self.show()

class API():
    def getDate(self):
        currentDate = datetime.today().strftime('%Y%m%d')
        print(f'Date: {currentDate}')
        return(currentDate)

    def getDefaultInfo(self):
        currencyToGet = ['USD', 'EUR']
        gotRate = []
        date = self.getDate()
        for currency in currencyToGet:
            # BASE_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20200604&json'
            BASE_URL = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency}&date={date}&json'
            response = requests.get(f"{BASE_URL}")
            gotRate.append(response.json()[0]['rate'])
        print(f"gotRate: {gotRate}")
        return(
            (currencyToGet, gotRate)
            )

    def createRows(self, gui, countOfRows):
        for _ in range(countOfRows):
            rowPosition = gui.ui.tableWidget.rowCount()
            gui.ui.tableWidget.insertRow(rowPosition)

    def fillTable(self, gui, currencyRate):
        # MainWindow.ui.tableWidget
        # ui.tableWidget.setItem(0, 0, "cellinfo")
        print(f'len value: {len(currencyRate[0])}')
        
        for row in range(len(currencyRate[0])):
            for column in range(2):

                cellinfo = QTableWidgetItem(str(currencyRate[column][row]))
                gui.ui.tableWidget.setItem(row, column, cellinfo)

    def greetingText(self, gui):
        """
        Set greeting text to label upon the time
        """
        actualHour = datetime.now().hour
        if (actualHour >= 6 and actualHour < 11):
            gui.ui.label.setText("Доброе утро")
        elif (actualHour >= 11 and actualHour < 18):
            gui.ui.label.setText("Добрый день")
        elif (actualHour >= 18 and actualHour < 21):
            gui.ui.label.setText("Добрый вечер")
        else:
            gui.ui.label.setText("Доброй ночи")

    def __init__(self, gui):

        currencyRate = self.getDefaultInfo()
        self.createRows(gui, len(currencyRate[0]))
        self.fillTable(gui, currencyRate)

        self.greetingText(gui) # change the greeting text upon the time


# Launch
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())