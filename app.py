import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

with open('config.json', 'r') as file:
    # file.read() grabs content of file
    config = json.loads(file.read())
    URL = config['URL']

desired_price = input()
page = urlopen(URL)

soup = BeautifulSoup(page, 'html.parser')
title = soup.find(id="productTitle").get_text().strip()  # remove whitespace
price = soup.find(id="priceblock_ourprice").get_text()
price = math.floor(float(price[1:]))  # round down and convert price to int


def check_price(desired_price, item_price):
    """Compare the current price of the item to the desired price.
    If current price is less than or equal to desired price, send notification.

    Arguments:
        desired_price {int} -- Desired price of item
        item_price {int} -- Current price of item
    """

    # Type check desire_price
    if isinstance(desired_price, int) is False:
        raise TypeError('desired_price must be int')
    else:
        if(desired_price < item_price):
            print('price still above your desired')
        if(desired_price >= item_price):
            # TODO: SEND NOTIFICATION
