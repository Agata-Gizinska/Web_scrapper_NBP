#!/usr/bin/env python3

# This program scraps info from Polish National Bank website about today's
# currency rate (USD, EUR, CHF, GBP, JPY) to PLN, and prints the output in
# a table.

import requests
from bs4 import BeautifulSoup
import pandas
import re
from datetime import datetime


def get_url():
    bank_website = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"
    return bank_website


def scrap_and_print(url):
    today = datetime.now().strftime('%d %B %Y %X')
    headings = []
    content = []
    currency = {'USD': {'EN': 'american dollar', 'PL': 'dolar amerykański'},
                'EUR': {'EN': 'euro', 'PL': 'euro'},
                'CHF': {'EN': 'swiss franc', 'PL': 'frank szwajcarski'},
                'GBP': {'EN': 'british pound sterling',
                        'PL': 'funt szterling'},
                'JPY': {'EN': 'japanese yen', 'PL': 'jen (Japonia)'}
                }

    # request HTML content from the website
    html_content = requests.get(url).text
    # create soup
    soup = BeautifulSoup(html_content, 'lxml')
    # find necessary website components
    table = soup.find('table', attrs={'class': 'nbptable'})
    body = table.find_all('tr')
    # prepare initial data for output table
    head = body[0]
    body_rows = body[1:]

    # process initial data to create output table column names
    for item in head.find_all('th'):
        item = item.text.rstrip('\n')  # strip new lines
        headings.append(item)

    # process initial data to create clean data for column rows, which should
    # contain only items specified in currency variable
    for row_num in range(len(body_rows)):
        row = []
        # process data and append to row variable
        for row_item in body_rows[row_num].find_all('td'):
            entry = re.sub('(\xa0)|(\n)', '', row_item.text)
            row.append(entry)
        # check if row variable contains Polish name of searched currency
        if len(row) >= 1:
            row = [x for x in row for item in currency.values() for r in row
                   if r in item.get('PL')]
            if row:
                content.append(row)  # if yes, append row to content
            else:
                continue  # if no, continue iteration

    # create a Dataframe for output table
    dataframe = pandas.DataFrame(data=content, columns=headings)
    output = dataframe.head()
    # move rows index by 1, so the output table begins from 1
    output.index += 1
    # print output table
    print('Currency rates for: ', today)
    print(output)


def main():
    scrap_and_print(get_url())


if __name__ == '__main__':
    main()
