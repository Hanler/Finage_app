from main import *
import requests

class API():
    def __init__(self): 
        BASE_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20200604&json'
        response = requests.get(f"{BASE_URL}")
        print(response.json())
        euro = response.json()[0]['rate']
        print(f"Euro: {euro}")


    def defaultInfo(self):
        pass