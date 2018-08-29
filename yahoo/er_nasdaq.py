import numpy as np
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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
    ret['ticker'] = ticker[:-1].replace('.', '-')
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
    try:
        browser.get(url)
    except TimeoutException:
        print('Timeout when accessing ' + url)
    html_source = browser.page_source
    soup = bs.BeautifulSoup(html_source, "lxml")
    tables = soup.find_all('table')
    confirmed = []
    unconfirmed = []
    for table in tables:
        tpattrs = table.parent.parent.attrs
        if 'id' in tpattrs and tpattrs['id'] == '_confirmed':
            df = parse_table(table, has_index=False)
            df = df[df.columns[1:]]
            confirmed = [parse_row(df.iloc[i]) for i in range(len(df))]
            links = table.find_all('a')
            times = []
            for ilink in range(len(links)):
                if not str(links[ilink]).startswith('<a href="https://www.nasdaq.com/earnings/report/'):
                    continue
                if ilink + 1 >= len(links) or str(links[ilink + 1]).startswith('<a href="https://www.nasdaq.com/earnings/report/'):
                    times.append('N/A')
                else:
                    times.append(links[ilink + 1].attrs['title'])
            if len(times) != len(confirmed):
                raise ValueError('Size mismatch between er times and infos!')
            for i in range(len(confirmed)):
                confirmed[i]['time'] = times[i]
        elif 'id' in tpattrs and tpattrs['id'] == '_unconfirmed':
            df = parse_table(table, has_index=False)
            unconfirmed = [parse_row(df.iloc[i]) for i in range(len(df))]
    return {
        'confirmed': confirmed,
        'unconfirmed': unconfirmed
    }


if __name__ == '__main__':
    import pickle
    import os
    date = datetime.datetime(2018, 6, 12)
    folder = "E:\\Data\\USFundamentals"
    browser = webdriver.Chrome()
    data = get_nasdaq_earnings_calendar(date, browser)
    browser.quit()
    pickle.dump(data, open(os.path.join(folder, 'er_nasdaq_' + date.strftime('%Y%m%d') + '.pkl'), 'wb'))
    print('Done')
