import numpy as np
import datetime
import json
from selenium import webdriver
import bs4 as bs
from utils import parse_table


def parse_float(s):
    if s == 'N/A' or s == '-' or s[0] == '∞':
        return np.nan
    s = s.replace(',', '')
    suffix = s[-1]
    if suffix in '0123456789':
        return float(s)
    try:
        f = float(s[:-1])
    except ValueError:
        raise ValueError('Cannot parse float: ' + str(s))
    if suffix == 'B':
        return f * 1e9
    if suffix == 'M':
        return f * 1e6
    if suffix.lower() == 'k':
        return f * 1e3
    if suffix == '%':
        return f / 100.0
    if suffix == 'T':
        return f * 1e12
    raise ValueError('Failed to parse float: ' + str(s))


def parse_fraction(s):
    if s == 'N/A' or s == '-':
        return np.nan
    infos = s.split('/')
    return float(infos[0]) / float(infos[1])


def parse_date(s):
    if s == 'N/A' or s == '-':
        return None
    return datetime.datetime.strptime(s, '%b %d, %Y')


def parse_type(s, value_type):
    if value_type == 'float':
        return parse_float(s)
    if value_type == 'date':
        return parse_date(s)
    if value_type == 'fraction':
        return parse_fraction(s)
    raise ValueError('Unknown Value Type: ' + str(value_type))


def parse_value(value):
    if type(value) is dict:
        value = float(value['raw']) if 'raw' in value else np.nan
    return value


def get_soup(ticker, tab, browser):
    URL = 'https://finance.yahoo.com/quote/{ticker}/{tab}?p={ticker}'
    url = URL.format(ticker=ticker, tab=tab)
    browser.get(url)
    html_source = browser.page_source
    return bs.BeautifulSoup(html_source, "lxml")


def get_raw_data(ticker, tab, browser, datastore='QuoteSummaryStore'):
    soup = get_soup(ticker, tab, browser)
    scripts = soup.find_all('script')
    for script in scripts:
        txt = script.text
        if 'root.App.main' in txt:
            all_data = json.loads(txt[:-12].split('root.App.main = ')[-1])
            break

    return all_data['context']['dispatcher']['stores'][datastore]


def parse_statistics(ticker, browser):
    soup = get_soup(ticker, 'key-statistics', browser)
    schema = [
        ['market_cap_intraday',             'Market Cap (intraday)',            'float'],
        ['enterprise_value',                'Enterprise Value',                 'float'],
        ['trailing_pe_ratio',               'Trailing P/E',                     'float'],
        ['forward_pe_ratio',                'Forward P/E',                      'float'],
        ['peg_ratio_5y_expected',           'PEG Ratio (5 yr expected)',        'float'],
        ['price_sales_ratio',               'Price/Sales',                      'float'],
        ['price_book_ratio',                'Price/Book',                       'float'],
        ['value_revenue_ratio',             'Enterprise Value/Revenue',         'float'],
        ['value_ebitda_ratio',              'Enterprise Value/EBITDA',          'float'],
        ['beta',                            'Beta',                             'float'],
        ['week52_change',                   '52-Week Change',                   'float'],
        ['week52_high',                     '52 Week High',                     'float'],
        ['week52_low',                      '52 Week Low',                      'float'],
        ['day50_moving_average',            '50-Day Moving Average',            'float'],
        ['day200_moving_average',           '200-Day Moving Average',           'float'],
        ['fiscal_year_ends',                'Fiscal Year Ends',                 'date'],
        ['most_recent_quarter',             'Most Recent Quarter',              'date'],
        ['profit_margin',                   'Profit Margin',                    'float'],
        ['operating_margin',                'Operating Margin',                 'float'],
        ['return_on_assets',                'Return on Assets',                 'float'],
        ['return_on_equity',                'Return on Equity',                 'float'],
        ['revenue',                         'Revenue',                          'float'],
        ['revenue_per_share',               'Revenue Per Share',                'float'],
        ['quarterly_revenue_growth',        'Quarterly Revenue Growth',         'float'],
        ['gross_profit',                    'Gross Profit',                     'float'],
        ['ebitda',                          'EBITDA',                           'float'],
        ['net_income_avi_to_common',        'Net Income Avi to Common',         'float'],
        ['diluted_eps',                     'Diluted EPS',                      'float'],
        ['quarterly_earnings_growth',       'Quarterly Earnings Growth',        'float'],
        ['total_cash',                      'Total Cash',                       'float'],
        ['total_cash_per_share',            'Total Cash Per Share',             'float'],
        ['total_debt',                      'Total Debt',                       'float'],
        ['total_debt_to_equity',            'Total Debt/Equity',                'float'],
        ['current_ratio',                   'Current Ratio',                    'float'],
        ['book_value_per_share',            'Book Value Per Share',             'float'],
        ['operating_cash_flow',             'Operating Cash Flow',               'float'],
        ['levered_free_cash_flow',          'Levered Free Cash Flow',           'float'],
        ['avg_vol_3m',                      'Avg Vol (3 month)',                'float'],
        ['avg_vol_10d',                     'Avg Vol (10 day)',                 'float'],
        ['shares_outstanding',              'Shares Outstanding',               'float'],
        ['shares_float',                    'Float',                            'float'],
        ['insiders_hold_ratio',             '% Held by Insiders',               'float'],
        ['institutions_hold_ratio',         '% Held by Institutions',           'float'],
        ['shares_short',                    'Shares Short',                     'float'],
        ['short_ratio',                     'Short Ratio',                      'float'],
        ['short_to_float_ratio',            'Short % of Float',                 'float'],
        ['shares_short_prev_month',         'Shares Short (prior month)',       'float'],
        ['forward_annual_dividend_rate',    'Forward Annual Dividend Rate',     'float'],
        ['forward_annual_dividend_yield',   'Forward Annual Dividend Yield',    'float'],
        ['trailing_annual_dividend_rate',   'Trailing Annual Dividend Rate',    'float'],
        ['trailing_annual_dividend_yield',  'Trailing Annual Dividend Yield',   'float'],
        ['average_dividend_yield_5y',       '5 Year Average Dividend Yield',    'float'],
        ['payout_ratio',                    'Payout Ratio',                     'float'],
        ['dividend_date',                   'Dividend Date',                    'date'],
        ['ex_dividend_date',                'Ex-Dividend Date',                 'date'],
        ['last_split_factor',               'Last Split Factor (new per old)',  'fraction'],
        ['last_split_date',                 'Last Split Date',                  'date'],
    ]
    results = {}
    for row in schema:
        key = row[0]
        value = row[1]
        value_type = row[2]
        ret = soup.find_all('span', text=value)
        if len(ret) == 0:
            raise RuntimeError('Failed to parse tag ' + str(value))
        if len(ret) > 1:
            if value != 'Most Recent Quarter':
                for r in ret:
                    print(r.text)
                    print(r.prettify())
                raise RuntimeError('Multiple results for tag ' + str(value))
        value_node = ret[0].parent.parent.contents[1]
        results[key] = parse_type(value_node.text, value_type)
    return results


def parse_analysis(ticker, browser):
    soup = get_soup(ticker, 'analysis', browser)
    tables = soup.find_all('table')
    wanted = {
        'Earnings Estimate':    'earnings_est',
        'Revenue Estimate':     'revenue_est',
        'Earnings History':     'earnings_history',
        'EPS Trend':            'eps_trend',
        'EPS Revisions':        'eps_revisions',
        'Growth Estimates':     'growth_est'
    }
    dfs = {}
    for table in tables:
        txt = table.text
        for w in wanted:
            if txt.startswith(w):
                df = parse_table(table)
                for col in df.columns:
                    df[col] = [parse_float(v) for v in df[col]]
                dfs[wanted[w]] = df
    results = {}
    if len(dfs) == 0:
        return results
    # Earnings Estimate
    tag = 'earnings_est'
    times = ['curr_qtr', 'next_qtr', 'curr_year', 'next_year']
    df = dfs[tag]
    index_map = {
        'n_analysts':   'No. of Analysts',
        'avg':          'Avg. Estimate',
        'low':          'Low Estimate',
        'high':         'High Estimate',
        'year_ago_eps': 'Year Ago EPS'
    }
    for index_key, index_value in index_map.items():
        row = df.ix[index_value]
        for i in range(4):
            results[tag + '.' + index_key + '.' + times[i]] = row[i]

    # Revenue Estimate
    tag = 'revenue_est'
    df = dfs[tag]
    index_map = {
        'n_analysts':       'No. of Analysts',
        'avg':              'Avg. Estimate',
        'low':              'Low Estimate',
        'high':             'High Estimate',
        'year_ago_sales':   'Year Ago Sales',
        'sales_growth':     'Sales Growth (year/est)'
    }
    for index_key, index_value in index_map.items():
        row = df.ix[index_value]
        for i in range(4):
            results[tag + '.' + index_key + '.' + times[i]] = row[i]

    # Earnings History
    tag = 'earnings_history'
    df = dfs[tag]
    index_map = {
        'eps_est':      'EPS Est.',
        'eps_actual':   'EPS Actual',
        'eps_diff':     'Difference',
        'surprise':     'Surprise %',
    }
    for index_key, index_value in index_map.items():
        row = df.ix[index_value]
        for i in range(4):
            results[tag + '.' + index_key + '.' + str(i + 1) + 'q'] = row[i]

    # Revenue Estimate
    tag = 'eps_trend'
    df = dfs[tag]
    index_map = {
        'est_curr':     'Current Estimate',
        'est_7d_ago':   '7 Days Ago',
        'est_30d_ago':  '30 Days Ago',
        'est_60d_ago':  '60 Days Ago',
        'est_90d_ago':  '90 Days Ago'
    }
    for index_key, index_value in index_map.items():
        row = df.ix[index_value]
        for i in range(4):
            results[tag + '.' + index_key + '.' + times[i]] = row[i]

    # EPS Revisions
    tag = 'eps_revisions'
    df = dfs[tag]
    index_map = {
        'up_last_7d':       'Up Last 7 Days',
        'up_last_30d':      'Up Last 30 Days',
        'down_last_7d':     'Down Last 7 Days',
        'down_last_30d':    'Down Last 30 Days'
    }
    for index_key, index_value in index_map.items():
        row = df.ix[index_value]
        for i in range(4):
            results[tag + '.' + index_key + '.' + times[i]] = row[i]

    # Growth Estimates
    tag = 'growth_est'
    values = dfs[tag][ticker]
    index_map = {
        'curr_qtr':             'Current Qtr.',
        'next_qtr':             'Next Qtr.',
        'curr_year':            'Current Year',
        'next_year':            'Next Year',
        'next_5_years_annum':   'Next 5 Years (per annum)',
        'past_5_years_annum':   'Past 5 Years (per annum)'
    }
    for index_key, index_value in index_map.items():
        results[tag + '.' + index_key] = values[index_value]

    return results


def convertTag(tag):
    """ convert tag from abcDef to abc_def
    """
    indices = [0] + [i for i in range(len(tag)) if tag[i].isupper()] + [len(tag)]
    ltag = tag.lower()
    return '_'.join([ltag[indices[i]:indices[i + 1]] for i in range(len(indices) - 1)])


def parse_financials(ticker, browser):
    raw_data = get_raw_data(ticker, 'financials', browser)
    tag_mapping = {
        'balanceSheetHistory': 'balance_annual',
        'balanceSheetHistoryQuarterly': 'balance_quarterly',
        'cashflowStatementHistory': 'cashflow_annual',
        'cashflowStatementHistoryQuarterly': 'cashflow_quarterly',
        'incomeStatementHistory': 'income_annual',
        'incomeStatementHistoryQuarterly': 'income_quarterly'
    }
    results = {}
    for tag, data in raw_data.items():
        if tag not in tag_mapping:
            continue
        prefix = tag_mapping[tag]
        ret = {}
        for name, sub_data in data.items():
            if name == 'maxAge':
                continue
            for values in sub_data:
                d = datetime.datetime.strptime(values['endDate']['fmt'], '%Y-%m-%d')
                r = {}
                for field, value in values.items():
                    if field in ['endDate', 'maxAge']:
                        continue
                    r[convertTag(field)] = float(value['raw']) if 'raw' in value else np.nan
                ret[d] = r
        results[prefix] = ret
    return results


def parse_profile(ticker, browser):
    raw_data = get_raw_data(ticker, 'profile', browser)
    data = raw_data['assetProfile']
    ret_profile = {}
    ret_officers = []
    for tag, values in data.items():
        if tag == 'maxAge':
            continue
        if tag == 'companyOfficers':
            for v in values:
                ret = {}
                for field, value in v.items():
                    if field == 'maxAge':
                        continue
                    value = parse_value(value)
                    ret[convertTag(field)] = value
                ret_officers.append(ret)
        else:
            ret_profile[convertTag(tag)] = values
    return {'asset_profile': ret_profile, 'company_officers': ret_officers}


def parse_sustainability(ticker, browser):
    raw_data = get_raw_data(ticker, 'sustainability', browser)
    results = {}
    data = raw_data['esgScores']
    if len(data) == 1 and 'err' in data:
        return results
    for tag, values in data.items():
        if tag == 'maxAge':
            continue
        tag = convertTag(tag)
        if type(values) is dict:
            if 'raw' in values:
                values = float(values['raw']) if 'raw' in values else np.nan
            else:
                for subtag, value in values.items():
                    results[tag + '.' + subtag] = value
                continue
        results[tag] = values
    return results


def parse_holders(ticker, browser):
    raw_data = get_raw_data(ticker, 'holders', browser)
    results = {}
    wanted = [
        'fundOwnership',
        'insiderHolders',
        'insiderTransactions',
        'institutionOwnership',
        'majorDirectHolders'
    ]
    for category in wanted:
        data = raw_data[category]
        category = convertTag(category)
        ret = []
        for key, values in data.items():
            if key == 'maxAge':
                continue
            for item in values:
                r = {}
                for tag, value in item.items():
                    if tag == 'maxAge':
                        continue
                    value = parse_value(value)
                    r[convertTag(tag)] = value
                ret.append(r)
        results[category] = ret
    ret = {}
    category = 'netSharePurchaseActivity'
    values = raw_data[category]
    for tag, value in values.items():
        if tag == 'maxAge':
            continue
        value = parse_value(value)
        ret[convertTag(tag)] = value
    results[convertTag(category)] = ret
    return results


def parse_news(ticker, browser):
    soup = get_soup(ticker, 'chart', browser)
    scripts = soup.find_all('script')
    for script in scripts:
        txt = script.text
        if 'root.App.main' in txt:
            all_data = json.loads(txt[:-12].split('root.App.main = ')[-1])
            break
    # all_data = json.loads(soup.find_all('script')[-9].text[:-12].split('root.App.main = ')[-1])
    raw_data = all_data['context']['dispatcher']['stores']['StreamStore']['streams']
    for key, data in raw_data.items():
        if ticker in key:
            raw_data = data['data']['stream_items']
            break
    news = []
    fields = [
        'publisher',
        'pubtime',
        'summary',
        'title',
        'type',
        'url'
    ]
    tags = [convertTag(field) for field in fields]
    for item in raw_data:
        if item['type'] == 'ad':
            continue
        values = [item[field] for field in fields]
        news.append(dict(zip(tags, values)))
    return news


def parse_yahoo_data(ticker, browser, ntry=3):
    results = {}
    funcs = [
        ('news', parse_news),
        ('holders', parse_holders),
        ('analysis', parse_analysis),
        ('statistics', parse_statistics),
        ('financials', parse_financials),
        ('profile', parse_profile),
        ('sustainability', parse_sustainability),
    ]
    has_error = False
    for info in funcs:
        itry = 0
        while itry < ntry:
            try:
                results[info[0]] = info[1](ticker, browser)
                break
            except Exception as e:
                has_error=True
                itry += 1
                if itry >= ntry:
                    browser.quit()
                    raise e
                browser.quit()
                browser = webdriver.Chrome()
    if has_error:
        browser.quit()

    # results['news'] = parse_news(ticker, browser)
    # results['holders'] = parse_holders(ticker, browser)
    # results['analysis'] = parse_analysis(ticker, browser)
    # results['statistics'] = parse_statistics(ticker, browser)
    # results['financials'] = parse_financials(ticker, browser)
    # results['profile'] = parse_profile(ticker, browser)
    # results['sustainability'] = parse_sustainability(ticker, browser)
    return results, has_error


def parse_yahoo_earnings_calendar(date, browser):
    URL = 'https://finance.yahoo.com/calendar/earnings?day={datestr}'
    datestr = date.strftime('%Y-%m-%d')
    url = URL.format(datestr=datestr)
    browser.get(url)
    html_source = browser.page_source
    soup = bs.BeautifulSoup(html_source, "lxml")

    scripts = soup.find_all('script')
    for script in scripts:
        txt = script.text
        if 'root.App.main' in txt:
            all_data = json.loads(txt[:-12].split('root.App.main = ')[-1])
            break

    raw_data = all_data['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
    data = []
    for item in raw_data:
        ecall = item['startdatetimetype']
        data.append({
            'ticker':               item['ticker'],
            'company':              item['companyshortname'],
            'earnings_date':        date,
            'earnings_call_time':   'After Market Close' if ecall == 'AMC' else 'Before Market Open' if ecall == 'BMO' else 'Time Not Supplied' if ecall == 'TNS' else None,
            'eps_estimate':         item['epsestimate']
        })
    return data


if __name__ == '__main__':
    tickers = [
        'TSLA',
    ]

    import pickle
    import os
    folder = "E:\\Data\\USFundamentals"
    browser = webdriver.Chrome()
    # yahoo_calendar = parse_yahoo_earnings_calendar(datetime.datetime(2018, 6, 18), browser)
    for ticker in tickers:
        print('Processing', ticker)
        results = parse_yahoo_data(ticker, browser)
        pickle.dump(results, open(os.path.join(folder, ticker + '.pkl'), 'wb'))
    browser.quit()
    print('Done')