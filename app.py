import json
import math
import time
from bs4 import BeautifulSoup
from twilio.rest import Client
from urllib.request import urlopen

with open('config.json', 'r') as file:
    # file.read() grabs content of file
    config = json.loads(file.read())
    URL = config['URL']
    account_sid = config['ACCOUNT_SID']
    auth_token = config['AUTH_TOKEN']

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
            send_notification(desired_price, item_price)


def send_notification(desired_price, item_price):
    """Sends SMS notification with prices and item name

    Arguments:
        desired_price {int} -- Desired price of item
        item_price {int} -- Current price of item
    """

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Current price for {title} is ${item_price}. Your deisred price is ${desired_price}. {URL}',
        from_='+twilio_number',
        to='+user_phone_number'
    )


while True:
    check_price(200, price)
    time.sleep((60 * 60) * 12)  # check every 12 hours
