import pickle
import os
import datetime
import time
import math
import yahoo.models as models
from yahoo.models import *
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


def yahoo_earnings_calendar_to_db(folder, date):
    filename = get_yahoo_er_filename(folder, date)
    create_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    data = pickle.load(open(filename, 'rb'))
    for item in data:
        record = EarningsCalendar(
            updated_on=create_time,
            is_confirmed=None,
            ticker=item['ticker'],
            full_name=item['company'],
            fiscal_quarter_ending='N/A',
            earnings_date=item['earnings_date'],
            time=item['earnings_call_time'] if item['earnings_call_time'] is not None else 'N/A',
            consensus_eps_forecast=None if math.isnan(item['eps_estimate']) else item['eps_estimate'],
            n_estimates=None,
            source='Yahoo'
        )
        record.save()


def yahoo_data_to_db(data, earnings, create_time):
    row = YahooStatistics(ref_earnings=earnings, updated_on=create_time, **data['statistics'])
    row.save()
    row = YahooNews(ref_earnings=earnings, updated_on=create_time, **data['news'])
    row.save()
    row = YahooSustainability(ref_earnings=earnings, updated_on=create_time, **data['sustainability'])
    row.save()

    data_financials = data['financials']
    for prefix, ret in data_financials.items():
        infos = prefix.split('_')
        row_class = infos[0]
        row_class[0] = row_class[0].upper()
        row_class = getattr(models, 'YahooFinancials' + row_class)
        report_freq = infos[1]
        report_freq[0] = report_freq[0].upper()
        for d, r in ret.items():
            row = row_class(ref_earnings=earnings, updated_on=create_time, report_freq=report_freq, report_date=d, **r)
            row.save()

    data_analysis = data['analysis']
    reports = {}
    for d, r in data_analysis.items():
        infos = d.split('.')
        data_type = infos[0].replace('_est', '_estimate')
        data_type_infos = data_type.split('_')
        data_type_infos = [t.capitalize() for t in data_type_infos]
        data_type = ''.join(data_type_infos)
        if data_type not in reports:
            reports[data_type] = {}
        if data_type == 'GrowthEstimate':
            reports[data_type][infos[-1]] = r
        else:
            if infos[1] not in reports[data_type]:
                reports[data_type][infos[1]] = {}
            reports[data_type][infos[1]][infos[-1]] = r
    for d, r in reports.items():
        if d == 'GrowthEstimate':
            row = YahooAnalysisGrowthEstimate(ref_earnings=earnings, updated_on=create_time, **r)
            row.save()
        else:
            row_class = getattr(models, 'YahooAnalysis' + d)
            for report_type, reprot_data in r.items():
                row = row_class(ref_earnings=earnings, updated_on=create_time, report_type=report_type, **report_data)
                row.save()

    data_holders = data['holders']
    for prefix, ret in data_holders.items():
        if prefix.endswith('_ownership'):
            owner_type = prefix.split('_')[0]
            for r in ret:
                row = YahooHoldersOwnership(ref_earnings=earnings, updated_on=create_time, owner_type=owner_type, **r)
                row.save()
        elif prefix.endswith('_holders'):
            holder_type = prefix.split('_')[0]
            for r in ret:
                row = YahooHoldersHolders(ref_earnings=earnings, updated_on=create_time, holder_type=holder_type, **r)
                row.save()
        elif prefix == 'insider_transactions':
            for r in ret:
                row = YahooHoldersInsiderTransactions(ref_earnings=earnings, updated_on=create_time, **r)
                row.save()
        elif prefix == 'net_share_purchase_activity':
            row = YahooHoldersNetSharePurchaseActivity(ref_earnings=earnings, updated_on=create_time, **ret)
            row.save()
        else:
            raise ValueError('Unknown report: ' + prefix)

    data_profile = data['profile']
    row = YahooProfileAssetProfile(ref_earnings=earnings, updated_on=create_time, **data_profile['asset_profile'])
    row.save()
    for r in data_profile['company_officers']:
        row = YahooProfileCompanyOfficers(ref_earnings=earnings, updated_on=create_time, **r)
        row.save()


if __name__ == '__main__':
    import pickle
    import os
    import datetime

    folder = "X:\\Trading\\USFundamentals"
    is_done = False
    curr_date = datetime.datetime.today().date()
    while True:
        now = datetime.datetime.now()
        print(now)
        if not is_done and now >= datetime.datetime.combine(curr_date, datetime.time(21, 0, 0)):
            next_date = curr_date + datetime.timedelta(days=1)
            if next_date.weekday() >= 5:
                curr_date = now.date()
            else:
                date = datetime.datetime.combine(next_date, datetime.time(0))
                print('Curr Time:', now, 'Target Date:', date)
                scrape_raw_data(folder, date)
                is_done = True
                curr_date = date.date()
        elif is_done and now.date() >= curr_date:
            is_done = False
        time.sleep(60)
    # nasdaq_earnings_calendar_to_db(folder, date)
    # yahoo_earnings_calendar_to_db(folder, date)
