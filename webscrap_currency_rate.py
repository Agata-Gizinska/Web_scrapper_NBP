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


def get_currency():
    currency = {
        'USD': {'EN': 'american dollar', 'PL': 'dolar amerykański'},
        'EUR': {'EN': 'euro', 'PL': 'euro'},
        'CHF': {'EN': 'swiss franc', 'PL': 'frank szwajcarski'},
        'GBP': {'EN': 'british pound sterling',
                'PL': 'funt szterling'},
        'JPY': {'EN': 'japanese yen', 'PL': 'jen (Japonia)'}
        }
    return currency


class Webscrapper:
    
    def __init__(self, url, currency_dict):
        self.url = url
        self.currency = currency_dict
        self.headings = []
        self.content = []
        self.today = datetime.now().strftime('%d %B %Y %X')
        self.output = None
        
    def request_content(self):
        html_content = requests.get(self.url).text
        return html_content
    
    def get_html_components_and_prepare_data(self, html_content):
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
            self.headings.append(item)
        # process initial data to create clean data for column rows, which should
        # contain only items specified in currency attribute
        for row_num in range(len(body_rows)):
            row = []
            # process data and append to row variable
            for row_item in body_rows[row_num].find_all('td'):
                entry = re.sub('(\xa0)|(\n)', '', row_item.text)
                row.append(entry)
            # check if row variable contains Polish name of searched currency
            if len(row) >= 1:
                row = [x for x in row for item in self.currency.values() for r in row
                    if r in item.get('PL')]
                if row:
                    self.content.append(row)  # if yes, append row to content
                else:
                    continue  # if no, continue iteration
        return self.headings, self.content
    
    def create_dataframe(self):
        dataframe = pandas.DataFrame(data=self.content, columns=self.headings)
        self.output = dataframe.head()
        # move rows index by 1, so the output table begins from 1
        self.output.index += 1
        return self.output
    
    def print_output(self):
        if self.output is not None:
            print('Currency rates for: ', self.today)
            print(self.output)
        else:
            print('Sorry, output table in not available.')


def main():
    webscrapper = Webscrapper(get_url(), get_currency())
    html_content = webscrapper.request_content()
    webscrapper.get_html_components_and_prepare_data(html_content)
    webscrapper.create_dataframe()
    webscrapper.print_output()


if __name__ == '__main__':
    main()
