import requests
from bs4 import BeautifulSoup

def get_stock_info(ticker):
    # ticker = 'SBIN' # Ticker
    exchange = 'NSE' # NSE, BOM
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    class1 = "YMlKec fxKbKc"
    price = float(soup.find(class_= class1).text.strip()[1:].replace(",",""))
    return price

