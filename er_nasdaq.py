import json
import datetime
from selenium import webdriver
import bs4 as bs
from utils import parse_table


def get_nasdaq_earnings_calendar(date, browser):
    URL = 'https://www.nasdaq.com/earnings/earnings-calendar.aspx?date={datestr}'
    datestr = date.strftime('%Y-%b-%d')
    url = URL.format(datestr=datestr)
    browser.get(url)
    html_source = browser.page_source
    soup = bs.BeautifulSoup(html_source, "lxml")
    tables = soup.find_all('table')
    return parse_table(tables[0])


if __name__ == '__main__':
    import pickle
    import os
    date = datetime.datetime(2018, 6, 11)
    folder = "E:\\Data\\USFundamentals"
    browser = webdriver.Chrome()
    data = get_nasdaq_earnings_calendar(date, browser)
    browser.quit()
    print('Done')
