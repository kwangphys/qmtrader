if __name__ == '__main__':
    import pickle
    import os
    import datetime
    from selenium import webdriver
    from er_nasdaq import *
    from yahoo import *

    date = datetime.datetime(2018, 6, 11)
    folder = "E:\\Data\\USFundamentals"
    browser = webdriver.Chrome()
    ercal = get_nasdaq_earnings_calendar(date, browser)
    datestr = date.strftime('%Y%m%d')
    pickle.dump(ercal, open(os.path.join(folder, 'er_nasdaq_' + datestr + '.pkl'), 'wb'))
    subfolder = os.path.join(folder, datestr)
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    for info in ercal['confirmed']:
        ticker = info['ticker']
        print('Processing', ticker)
        results = parse_yahoo_data(ticker, browser)
        pickle.dump(results, open(os.path.join(subfolder, ticker + '.pkl'), 'wb'))
    for info in ercal['unconfirmed']:
        ticker = info['ticker']
        print('Processing', ticker)
        results = parse_yahoo_data(ticker, browser)
        pickle.dump(results, open(os.path.join(subfolder, ticker + '.pkl'), 'wb'))
    browser.quit()
    print('Done')
