from yahoo.tasks import *
from yahoo.yahoo import *
from yahoo.er_nasdaq import *


def scrape_one_day(d, folder):
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(30)
    data = get_nasdaq_post_earnings_calendar(d, browser)
    if len(data) > 0:
        pickle.dump(data, open(get_nasdaq_post_er_filename(folder, d), 'wb'))
        nasdaq_post_earnings_calendar_to_db(folder, d)
    browser.quit()

    browser = webdriver.Chrome()
    browser.set_page_load_timeout(30)
    data = parse_yahoo_post_earnings_calendar(d, browser)
    if len(data) > 0:
        pickle.dump(data, open(get_yahoo_post_er_filename(folder, d), 'wb'))
        yahoo_post_earnings_calendar_to_db(folder, d)
    browser.quit()


if __name__ == '__main__':
    import datetime
    start_date = datetime.datetime(2018, 6, 8)
    end_date = datetime.datetime.today()
    folder = "E:\\Data\\USFundamentals"
    d = start_date
    while d < end_date:
        print(d)
        scrape_one_day(d, folder)
        d = d + datetime.timedelta(days=1)
    print('Done')

