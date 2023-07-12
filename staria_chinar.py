#!/usr/bin/python

"""Fetch Staria Chinar Sofia lunch menu for the day"""

import sys
from datetime import date
from bs4 import BeautifulSoup
import requests

current_date    = date.today().strftime('%d.%m')

menu_dict       = {}
MAX_LEN         = 0

URL = "https://obednomenu.stariachinar.com/sofia/"

try:
    html_content = requests.get(URL, timeout=5).text

except requests.exceptions.RequestException as e:
    print(f'Страницата не може да бъде заредена: {e}')
    sys.exit(1)

try:
    soup = BeautifulSoup(html_content, "lxml")

    monday      = soup.select('#wrapper > section:nth-child(4) > div.container > div > div > div > div > div > div')
    tuesday     = soup.select('#wrapper > section:nth-child(5) > div.container > div > div > div > div > div > div')
    wednesday   = soup.select('#wrapper > section:nth-child(6) > div.container > div > div > div > div > div > div')
    thursday    = soup.select('#wrapper > section:nth-child(7) > div.container > div > div > div > div > div > div')
    friday      = soup.select('#wrapper > section:nth-child(8) > div.container > div > div > div > div > div > div')


    week = [monday, tuesday, wednesday, thursday, friday]

    for day in week:
        if day[0].span.get_text() == current_date:
            today = day[0]

    today_date = today.span.extract().get_text()
    today_name = today.h2.get_text()

    menu_category = today.select('h4')

except Exception as e:
    print(f'Грешка при обработка на HTML: {e}')
    sys.exit(1)

for index, category_item in enumerate(menu_category):

    category = category_item.get_text()

    menu_dict[category] = []

    table       = category_item.find_next('table')
    menu_item   = table.select('tbody > tr > th > h5 > span')
    item_price  = table.select('tbody > tr > td > h5')

    # Expectation is that each item has a name and price, so iterate over both
    for item, price in zip(menu_item, item_price):

        item_len = len(item.get_text())

        # Check for length of item for final pretty printing
        MAX_LEN = max(MAX_LEN, item_len)

        # Create packed dictionary with list of items inside
        menu_dict[category].append({"name" : item.get_text(), "price" : price.get_text()})


# Final formamatted printing
print(f"{today_name} {today_date}")
print(f"{'=' * (len(today_name) + len(today_date) + 1)}")

for key, value in menu_dict.items():

    print(f"\n{key}\n{'-' * len(key)}\n")

    for item in value:
        print(f"{item['name']:{MAX_LEN}}\t{item['price']}")
