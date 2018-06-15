import pickle
import os
import datetime
from yahoo.models import *
from selenium import webdriver
from yahoo.er_nasdaq import *
from yahoo.yahoo import *


def get_nasdaq_er_filename(folder, date):
    datestr = date.strftime('%Y%m%d')
    return os.path.join(folder, 'er_nasdaq_' + datestr + '.pkl')


def get_yahoo_fundamental_filename(folder, date, ticker):
    datestr = date.strftime('%Y%m%d')
    subfolder = os.path.join(folder, datestr)
    return os.path.join(subfolder, ticker + '.pkl')


def scrape_raw_data(folder, date):
    browser = webdriver.Chrome()
    ercal = get_nasdaq_earnings_calendar(date, browser)
    datestr = date.strftime('%Y%m%d')
    pickle.dump(ercal, open(get_nasdaq_er_filename(folder, date), 'wb'))
    subfolder = os.path.join(folder, datestr)
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    for info in ercal['confirmed']:
        ticker = info['ticker']
        ticker_filename = get_yahoo_fundamental_filename(folder, date, ticker)
        print('Processing', ticker)
        results = parse_yahoo_data(ticker, browser)
        pickle.dump(results, open(ticker_filename, 'wb'))
    for info in ercal['unconfirmed']:
        ticker = info['ticker']
        ticker_filename = get_yahoo_fundamental_filename(folder, date, ticker)
        print('Processing', ticker)
        results = parse_yahoo_data(ticker, browser)
        pickle.dump(results, open(ticker_filename, 'wb'))
    browser.quit()
    print('Done')


def nasdaq_earnings_calendar_to_db(folder, date):
    filename = get_nasdaq_er_filename(folder, date)
    create_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    data = pickle.load(open(filename, 'rb'))
    for item in data['confirmed']:
        record = NasdaqEarningsCalendar(
            updated_on=create_time,
            is_confirmed=True,
            ticker=item['ticker'],
            full_name=item['full_name'],
            fiscal_quarter_ending=item['fiscal_quarter_ending'],
            earnings_date=item['earnings_date'].date(),
            time=item['time'],
            consensus_eps_forecast=item['consensus_eps_forecast'],
            n_estimates=item['n_estimates']
        )
        record.save()
    for item in data['unconfirmed']:
        record = NasdaqEarningsCalendar(
            updated_on=create_time,
            is_confirmed=False,
            ticker=item['ticker'],
            full_name=item['full_name'],
            fiscal_quarter_ending=item['fiscal_quarter_ending'],
            earnings_date=item['earnings_date'].date(),
            consensus_eps_forecast=item['consensus_eps_forecast'],
            n_estimates=item['n_estimates'],
            time='N/A'
        )
        record.save()


if __name__ == '__main__':
    import pickle
    import os
    import datetime

    date = datetime.datetime(2018, 6, 11)
    folder = "X:\\Trading\\USFundamentals"
    # scrape_raw_data(folder, date)
    nasdaq_earnings_calendar_to_db(folder, date)