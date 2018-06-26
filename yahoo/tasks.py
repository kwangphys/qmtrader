import pickle
import os
import datetime
import math
from yahoo.models import *
from selenium import webdriver
from yahoo.er_nasdaq import *
from yahoo.yahoo import *


def get_nasdaq_er_filename(folder, date):
    datestr = date.strftime('%Y%m%d')
    return os.path.join(folder, 'er_nasdaq_' + datestr + '.pkl')


def get_yahoo_er_filename(folder, date):
    datestr = date.strftime('%Y%m%d')
    return os.path.join(folder, 'er_yahoo_' + datestr + '.pkl')


def get_yahoo_fundamental_filename(folder, date, ticker):
    datestr = date.strftime('%Y%m%d')
    subfolder = os.path.join(folder, datestr)
    return os.path.join(subfolder, ticker + '.pkl')


def scrape_raw_data(folder, date):
    browser = webdriver.Chrome()
    datestr = date.strftime('%Y%m%d')
    er_nasdaq_cal = get_nasdaq_earnings_calendar(date, browser)
    nasdaq_tickers = [v['ticker'] for v in er_nasdaq_cal['confirmed']] + [v['ticker'] for v in er_nasdaq_cal['unconfirmed']]
    if len(nasdaq_tickers) > 0:
        pickle.dump(er_nasdaq_cal, open(get_nasdaq_er_filename(folder, date), 'wb'))
    er_yahoo_cal = parse_yahoo_earnings_calendar(date, browser)
    yahoo_tickers = [v['ticker'] for v in er_yahoo_cal]
    if len(yahoo_tickers) > 0:
        pickle.dump(er_yahoo_cal, open(get_yahoo_er_filename(folder, date), 'wb'))
    subfolder = os.path.join(folder, datestr)
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    tickers = list(set(nasdaq_tickers + yahoo_tickers))
    tickers.sort()
    for ticker in tickers:
        ticker_filename = get_yahoo_fundamental_filename(folder, date, ticker)
        print('Processing', ticker)
        try:
            results, has_error = parse_yahoo_data(ticker, browser)
            pickle.dump(results, open(ticker_filename, 'wb'))
            if has_error:
                browser = webdriver.Chrome()
        except Exception as e:
            print(e)
            browser = webdriver.Chrome()
    browser.quit()
    print('Done')


def nasdaq_earnings_calendar_to_db(folder, date):
    filename = get_nasdaq_er_filename(folder, date)
    create_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    data = pickle.load(open(filename, 'rb'))
    for item in data['confirmed']:
        record = EarningsCalendar(
            updated_on=create_time,
            is_confirmed=True,
            ticker=item['ticker'],
            full_name=item['full_name'],
            fiscal_quarter_ending=item['fiscal_quarter_ending'],
            earnings_date=item['earnings_date'].date(),
            time=item['time'],
            consensus_eps_forecast=None if math.isnan(item['consensus_eps_forecast']) else item['consensus_eps_forecast'],
            n_estimates=item['n_estimates'],
            source='Nasdaq'
        )
        record.save()
    for item in data['unconfirmed']:
        record = EarningsCalendar(
            updated_on=create_time,
            is_confirmed=False,
            ticker=item['ticker'],
            full_name=item['full_name'],
            fiscal_quarter_ending=item['fiscal_quarter_ending'],
            earnings_date=item['earnings_date'].date(),
            consensus_eps_forecast=None if math.isnan(item['consensus_eps_forecast']) else item['consensus_eps_forecast'],
            n_estimates=item['n_estimates'],
            time='N/A',
            source='Nasdaq'
        )
        record.save()


if __name__ == '__main__':
    import pickle
    import os
    import datetime

    date = datetime.datetime(2018, 6, 27)
    folder = "X:\\Trading\\USFundamentals"
    scrape_raw_data(folder, date)
    # nasdaq_earnings_calendar_to_db(folder, date)