from yahoo.tasks import *
from yahoo.yahoo import *
from yahoo.er_nasdaq import *


def scrape_one_day(d, folder, browser):
    data = get_nasdaq_post_earnings_calendar(d, browser)
    if len(data) > 0:
        pickle.dump(data, open(get_nasdaq_post_er_filename(folder, d), 'wb'))
        nasdaq_post_earnings_calendar_to_db(folder, d)

    data = parse_yahoo_post_earnings_calendar(d, browser)
    if len(data) > 0:
        pickle.dump(data, open(get_yahoo_post_er_filename(folder, d), 'wb'))
        yahoo_post_earnings_calendar_to_db(folder, d)


if __name__ == '__main__':
    import datetime
    date = datetime.datetime(2018, 5, 31)
    folder = "E:\\Data\\USFundamentals"
    browser = webdriver.Chrome()
    # browser.set_page_load_timeout(10)
    scrape_one_day(date, folder, browser)
    browser.quit()
    print('Done')

