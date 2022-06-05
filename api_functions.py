# from main import *
import requests
from datetime import datetime

from main import *

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

    def fillTable(self, currencyRate):
        # MainWindow.ui.tableWidget
        self.ui.tableWidget.setItem(0, 0, "cellinfo")

    def __init__(self):
        currencyRate = self.getDefaultInfo()
        self.fillTable(currencyRate)