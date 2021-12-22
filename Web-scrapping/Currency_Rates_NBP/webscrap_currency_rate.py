# This program scraps info from Polish National Bank website about today's
# currency rate (USD, EUR, CHF, GBP, JPY) to PLN, and prints the output in a table.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import date

today = date.today()
bank_website = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"
headings = []
content = []
currency = ['dolar amerykański', 'euro', 'frank szwajcarski', 'funt szterling', 'jen (Japonia)']


def extract_data(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.find('table', attrs={'class': 'nbptable'})
    body = table.find_all('tr')
    head = body[0]
    body_rows = body[1:]

    for item in head.find_all('th'):
        item = item.text.rstrip('\n')
        headings.append(item)

    for row_num in range(len(body_rows)):
        row = []
        for row_item in body_rows[row_num].find_all('td'):
            entry = re.sub('(\xa0)|(\n)', '', row_item.text)
            row.append(entry)
        while len(row) >= 1:
            check = any(item in row for item in currency)
            if check is True:
                content.append(row)
                break
            elif row in content:
                break
            else:
                break
    return headings, content


def show_results_in_table():
    dataframe = pd.DataFrame(data=content, columns=headings)
    output = dataframe.head()
    output.index += 1
    print('Currency rates for date:', today)
    print(output)


def main():
    extract_data(bank_website)
    show_results_in_table()


if __name__ == '__main__':
    main()
