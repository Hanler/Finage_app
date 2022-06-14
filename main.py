# Imports 
from gettext import find
import sys
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
from design_2 import Ui_CurrencyWindow

# Import functions
from ui_functions import *

# Defines

# Functions

# Classes

class CurrencyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CurrencyWindow()
        self.ui.setupUi(self)
        self.ui.currency_search.setPlaceholderText("Введите аббревиатуру валюты") # ?
        
        self.currency = ("AUD", "AZN", "BYN", "BGN", "KRW", "HKD", "DKK", "USD", "EUR", "EGP", "JPY", "PLN", "INR", "CAD", "HRK", "MXN", "MDL", "ILS", "NZD", "NOK", "ZAR", "RUB", "RON", "IDR", "SGD", "XDR", "KZT", "TRY", "HUF", "GBP", "CZK", "SEK", "CHF", "CNY")

        self.addCheckBoxes(self.currency)

        self.ui.currency_search.textChanged.connect(self.search)
        # self.search()

    def addCheckBoxes(self, arrCurrancy):
        """
        Initial adding of checkboxes
        """
        for i in range(len(arrCurrancy)):
            self.checkBox = QtWidgets.QCheckBox(self.ui.scrollAreaWidgetContents)
            font = QtGui.QFont()
            font.setFamily("Magistral Book")
            self.checkBox.setFont(font)
            self.checkBox.setObjectName(f"checkBox{i}")
            self.ui.verticalLayout_2.addWidget(self.checkBox)
            self.checkBox.setText(self.currency[i])

        # self.ui.checkBox.hide()
        self.ui.scrollAreaWidgetContents.findChild(QtWidgets.QCheckBox, "checkBox1").hide()

    def hideCheckboxes(self):
        """
        Hides all checkboxes in scrollAreaWidgetContents
        """
        amountOfChildElems = len( self.ui.scrollAreaWidgetContents.children() )
        for i in range(amountOfChildElems - 1):
            elemToHide = self.ui.scrollAreaWidgetContents.findChild(QtWidgets.QCheckBox, f"checkBox{i}")
            elemToHide.hide()

    def showCheckboxes(self, arrCurrancy):
        """
        Shows checkboxes from the argument array
        """
        for i in arrCurrancy:
            numberOfCheckbox = self.currency.index(i)
            self.ui.scrollAreaWidgetContents.findChild(QtWidgets.QCheckBox, f"checkBox{numberOfCheckbox}").show()

    def search(self):
        """
        Searches the abbreviation of currencies upon the request from the input
        """
        txt = self.ui.currency_search.toPlainText()
        txtUpperNorm = txt.upper().replace(' ', '')
        
        resultOfSearch = []
        for abbr in self.currency:
            print(f"The result of searching {txtUpperNorm} in {abbr}: {abbr.find(txtUpperNorm)}")
            if (abbr.find(txtUpperNorm) == 0):
                resultOfSearch.append(abbr)

        self.hideCheckboxes()
        self.showCheckboxes(resultOfSearch)

class MainWindow(QMainWindow):
    def __init__(self):
        # QMainWindow.__init__(self)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # super().__init__()

        # Toggle burger menu
        self.ui.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        # Connect buttons and methods
        self.ui.changeView.clicked.connect(self.createCurrencyWindow)

        # API initialize
        api = API(self)

        # Show main window
        self.show()
    
    def createCurrencyWindow(self):
        self.currencyWindow = CurrencyWindow(self)
        self.currencyWindow.show()

class API():
    def getDate(self):
        """
        Returns the current date in format YY:MM:DD
        """
        currentDate = datetime.today().strftime('%Y%m%d')
        return(currentDate)

    def getDefaultInfo(self):
        """
        Sends the default API for the currency rate (EUR and USD)
        """
        # TODO: change this function to make it for all cases (not only default) 
        currencyToGet = ['USD', 'EUR']
        gotRate = []
        date = self.getDate()
        for currency in currencyToGet:
            # BASE_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20200604&json'
            BASE_URL = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency}&date={date}&json'
            response = requests.get(f"{BASE_URL}")
            gotRate.append(response.json()[0]['rate'])
        return(
            (currencyToGet, gotRate)
            )

    def createRows(self, gui, countOfRows):
        """
        Creates as many rows in table as we need
        """
        for _ in range(countOfRows):
            rowPosition = gui.ui.tableWidget.rowCount()
            gui.ui.tableWidget.insertRow(rowPosition)

    def fillTable(self, gui, currencyRate):
        """
        Fills the table with the currency rate
        """
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

    def getNews(self):
        """
        Sends API for the latest news and prepares last new (title and author) 
        """
        # b557749026c044cfba6f7318dcff5298
        response = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=b557749026c044cfba6f7318dcff5298')
        print(f"JSON from response: {response.json()}")
        print(f"Part of full JSON: {response.json()['articles'][0]}")
        theLastArticle = response.json()['articles'][0]
        source = theLastArticle['source']['name']
        # content = theLastArticle['content']
        # print(f"straight content: {content}")
        # if (content is None):
        #     content = theLastArticle['title']
        # if( len(content) > 40):
        #     content = content[:280] + "..."
        content = theLastArticle['title']

        print(f"The aricle of the {source} is: {content}")
        return(
            (content, source)
        )

    def fillNews(self, gui, new):
        """
        Fill the labels for news with the prepared data
        """
        gui.ui.label_news.setText(new[0])
        gui.ui.label_author.setText(new[1])

    def __init__(self, gui):
        try:
            actualNew = self.getNews()
            self.fillNews(gui, actualNew)
        except:
            pass # TODO implement the button to retry sending API for news

        try: 
            currencyRate = self.getDefaultInfo()
            self.createRows(gui, len(currencyRate[0]))
            self.fillTable(gui, currencyRate)
        except:
            pass # TODO implement the button to retry sending API for currency rate

        self.greetingText(gui) # change the greeting text upon the time


# Launch
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())