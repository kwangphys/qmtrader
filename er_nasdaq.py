import json
import numpy as np
import datetime
from selenium import webdriver
import bs4 as bs
from utils import parse_table


def parse_row(row):
    ret = {}
    row = [r.replace('\n', '').replace('\t', '').strip() for r in row]
    infos = row[0].split('Market Cap')[0].rstrip()
    ticker = infos.split('(')[-1]
    ret['full_name'] = infos[:-len(ticker) - 1].rstrip()
    if ticker[-1] != ')':
        raise ValueError('Failed to parse ' + row[0])
    ret['ticker'] = ticker[:-1]
    ret['earnings_date'] = datetime.datetime.strptime(row[1], '%m/%d/%Y')
    ret['fiscal_quarter_ending'] = datetime.datetime.strptime(row[2], '%b %Y').strftime('%Y%m')
    eps = row[3][1:]
    ret['consensus_eps_forecast'] = np.nan if eps == 'n/a' else float(eps)
    ret['n_estimates'] = int(row[4])
    return ret


def get_nasdaq_earnings_calendar(date, browser):
    URL = 'https://www.nasdaq.com/earnings/earnings-calendar.aspx?date={datestr}'
    datestr = date.strftime('%Y-%b-%d')
    url = URL.format(datestr=datestr)
    browser.get(url)
    html_source = browser.page_source
    soup = bs.BeautifulSoup(html_source, "lxml")
    tables = soup.find_all('table')
    df = parse_table(tables[0])
    return [parse_row(df.iloc[i]) for i in range(len(df))]


if __name__ == '__main__':
    import pickle
    import os
    date = datetime.datetime(2018, 6, 11)
    folder = "E:\\Data\\USFundamentals"
    browser = webdriver.Chrome()
    data = get_nasdaq_earnings_calendar(date, browser)
    browser.quit()
    pickle.dump(data, open(os.path.join(folder, 'er_nasdaq_' + date.strftime('%Y%m%d') + '.pkl'), 'wb'))
    print('Done')
