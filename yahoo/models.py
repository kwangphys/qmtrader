from django.db import models as dm
from getpass import getuser


class DatedModel(dm.Model):

    updated_on = dm.DateTimeField(auto_now_add=True)
    updated_by = dm.CharField(max_length=64, default=getuser())

    class Meta:
        abstract = True


class EarningsCalendar(DatedModel):

    ticker = dm.CharField(max_length=16, null=False, blank=False)
    full_name = dm.CharField(max_length=255)
    fiscal_quarter_ending = dm.CharField(max_length=16, null=False, blank=False)
    earnings_date = dm.DateField(null=False)
    time = dm.CharField(max_length=32)
    consensus_eps_forecast = dm.FloatField(null=True)
    n_estimates = dm.IntegerField(null=True)
    is_confirmed = dm.NullBooleanField()
    source = dm.CharField(max_length=16)


class YahooStatistics(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    market_cap_intraday = dm.FloatField(null=False)
    enterprise_value = dm.FloatField(null=False)
    trailing_pe_ratio = dm.FloatField(null=True)
    forward_pe_ratio = dm.FloatField(null=True)
    peg_ratio_5y_expected = dm.FloatField(null=False)
    price_sales_ratio = dm.FloatField(null=False)
    price_book_ratio = dm.FloatField(null=False)
    value_revenue_ratio = dm.FloatField(null=False)
    value_ebitda_ratio = dm.FloatField(null=False)
    beta = dm.FloatField(null=False)
    week52_change = dm.FloatField(null=False)
    week52_high = dm.FloatField(null=False)
    week52_low = dm.FloatField(null=False)
    day50_moving_average = dm.FloatField(null=False)
    day200_moving_average = dm.FloatField(null=False)
    fiscal_year_ends = dm.DateField(null=False)
    most_recent_quarter = dm.DateField(null=False)
    profit_margin = dm.FloatField(null=False)
    operating_margin = dm.FloatField(null=False)
    return_on_assets = dm.FloatField(null=False)
    return_on_equity = dm.FloatField(null=False)
    revenue = dm.FloatField(null=False)
    revenue_per_share = dm.FloatField(null=False)
    quarterly_revenue_growth = dm.FloatField(null=False)
    gross_profit = dm.FloatField(null=False)
    ebitda = dm.FloatField(null=False)
    net_income_avi_to_common = dm.FloatField(null=False)
    diluted_eps = dm.FloatField(null=False)
    quarterly_earnings_growth = dm.FloatField(null=True)
    total_cash = dm.FloatField(null=False)
    total_cash_per_share = dm.FloatField(null=False)
    total_debt = dm.FloatField(null=False)
    total_debt_to_equity = dm.FloatField(null=False)
    current_ratio = dm.FloatField(null=False)
    book_value_per_share = dm.FloatField(null=False)
    operating_cash_flow = dm.FloatField(null=False)
    levered_free_cash_flow = dm.FloatField(null=False)
    avg_vol_3m = dm.FloatField(null=False)
    avg_vol_10d = dm.FloatField(null=False)
    shares_outstanding = dm.FloatField(null=False)
    shares_float = dm.FloatField(null=False)
    insider_hold_ratio = dm.FloatField(null=False)
    institutions_hold_ratio = dm.FloatField(null=False)
    shares_short = dm.FloatField(null=False)
    short_ratio = dm.FloatField(null=False)
    short_to_float_ratio = dm.FloatField(null=False)
    shares_short_prev_month = dm.FloatField(null=False)
    forward_annual_dividend_rate = dm.FloatField(null=True)
    forward_annual_dividend_yield = dm.FloatField(null=True)
    trailing_annual_dividend_rate = dm.FloatField(null=True)
    trailing_annual_dividend_yield = dm.FloatField(null=True)
    average_dividend_yield_5y = dm.FloatField(null=True)
    payout_ratio = dm.FloatField(null=False)
    dividend_date = dm.DateField(null=True)
    ex_dividend_date = dm.DateField(null=True)
    last_split_factor = dm.FloatField(null=True)
    last_split_date = dm.DateField(null=True)


class YahooFinancialsCashflow(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_date = dm.DateField(null=False)
    report_freq = dm.CharField(max_length=1, choices=(('q', 'Quarterly'), ('a', 'Annual')))
    net_income = dm.FloatField(null=True)
    depreciation = dm.FloatField(null=True)
    change_to_netincome = dm.FloatField(null=True)
    change_to_account_receivables = dm.FloatField(null=True)
    change_to_liabilities = dm.FloatField(null=True)
    change_to_inventory = dm.FloatField(null=True)
    change_to_operating_activities = dm.FloatField(null=True)
    total_cash_from_operating_activities = dm.FloatField(null=False)
    capital_expenditures = dm.FloatField(null=True)
    investments = dm.FloatField(null=True)
    other_cashflows_from_investing_activities = dm.FloatField(null=True)
    total_cashflows_from_investing_activities = dm.FloatField(null=False)
    dividend_paid = dm.FloatField(null=True)
    sale_purchase_of_stock = dm.FloatField(null=True)
    net_borrowings = dm.FloatField(null=True)
    other_cashflows_from_financing_activities = dm.FloatField(null=True)
    total_cash_from_financing_activities = dm.FloatField(null=False)
    effect_of_exchange_rate = dm.FloatField(null=True)
    change_in_cash = dm.FloatField(null=False)


class YahooFinancialsBalance(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_date = dm.DateField(null=False)
    report_freq = dm.CharField(max_length=1, choices=(('q', 'Quarterly'), ('a', 'Annual')))
    cash = dm.FloatField(null=True)
    short_term_investments = dm.FloatField(null=True)
    net_receivables = dm.FloatField(null=True)
    inventory = dm.FloatField(null=True)
    other_current_assets = dm.FloatField(null=True)
    total_current_assets = dm.FloatField(null=False)
    long_term_investments = dm.FloatField(null=True)
    property_plant_equipment = dm.FloatField(null=True)
    good_will = dm.FloatField(null=True)
    intangible_assets = dm.FloatField(null=True)
    accumulated_amortization = dm.FloatField(null=True)
    other_assets = dm.FloatField(null=True)
    deferred_long_term_assets = dm.FloatField(null=True)
    total_assets = dm.FloatField(null=False)
    account_payable = dm.FloatField(null=True)
    short_long_term_debt = dm.FloatField(null=True)
    other_current_liab = dm.FloatField(null=True)
    total_current_liabilities = dm.FloatField(null=False)
    long_term_debt = dm.FloatField(null=True)
    other_liab = dm.FloatField(null=True)
    deferred_long_term_liab = dm.FloatField(null=True)
    minority_interest = dm.FloatField(null=True)
    negative_good_will = dm.FloatField(null=True)
    total_liab = dm.FloatField(null=False)
    stock_option_warrants = dm.FloatField(null=True)
    redeemable_preferred_stock = dm.FloatField(null=True)
    preferred_stock = dm.FloatField(null=True)
    common_stock = dm.FloatField(null=True)
    retained_earnings = dm.FloatField(null=True)
    treasury_stock = dm.FloatField(null=True)
    capital_surplus = dm.FloatField(null=True)
    other_stockholder_equity = dm.FloatField(null=True)
    total_stockholder_equity = dm.FloatField(null=True)
    net_tangible_assets = dm.FloatField(null=False)


class YahooFinancialsIncome(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_date = dm.DateField(null=False)
    report_freq = dm.CharField(max_length=1, choices=(('q', 'Quarterly'), ('a', 'Annual')))
    total_revenue = dm.FloatField(null=False)
    cost_of_revenue = dm.FloatField(null=True)
    gross_profit = dm.FloatField(null=False)
    research_development = dm.FloatField(null=True)
    selling_general_administrative = dm.FloatField(null=True)
    non_recurring = dm.FloatField(null=True)
    other_operating_expenses = dm.FloatField(null=True)
    total_operating_expenses = dm.FloatField(null=True)
    operating_income = dm.FloatField(null=False)
    total_other_income_expense_net = dm.FloatField(null=True)
    ebit = dm.FloatField(null=True)
    interest_expense = dm.FloatField(null=True)
    income_before_tax = dm.FloatField(null=True)
    income_tax_expense = dm.FloatField(null=True)
    minority_interest = dm.FloatField(null=True)
    net_income_from_continuing_ops = dm.FloatField(null=False)
    discontinued_operations = dm.FloatField(null=True)
    extradinary_items = dm.FloatField(null=True)
    effect_of_accounting_changes = dm.FloatField(null=True)
    other_items = dm.FloatField(null=True)
    net_income = dm.FloatField(null=False)
    preferred_stock_and_other_adjustments = dm.FloatField(null=True)
    net_income_applicable_to_common_shares = dm.FloatField(null=True)


class YahooAnalysisEarningsEstimate(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_type = dm.CharField(max_length=16, null=False, blank=False)
    n_analysts = dm.IntegerField(null=False)
    avg = dm.FloatField(null=True)
    low = dm.FloatField(null=True)
    high = dm.FloatField(null=True)
    year_ago_eps = dm.FloatField(null=True)


class YahooAnalysisRevenueEstimate(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_type = dm.CharField(max_length=16, null=False, blank=False)
    n_analysts = dm.IntegerField(null=False)
    avg = dm.FloatField(null=True)
    low = dm.FloatField(null=True)
    high = dm.FloatField(null=True)
    year_ago_sales = dm.FloatField(null=True)
    sales_growth = dm.FloatField(null=True)


class YahooAnalysisEarningsHistory(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_type = dm.CharField(max_length=16, null=False, blank=False)
    eps_est = dm.FloatField(null=True)
    eps_actual = dm.FloatField(null=True)
    eps_diff = dm.FloatField(null=True)
    surprise = dm.FloatField(null=True)


class YahooAnalysisEPSTrend(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_type = dm.CharField(max_length=16, null=False, blank=False)
    eps_curr = dm.FloatField(null=True)
    eps_7d = dm.FloatField(null=True)
    eps_30d = dm.FloatField(null=True)
    eps_60d = dm.FloatField(null=True)
    eps_90d = dm.FloatField(null=True)


class YahooAnalysisEPSRevisions(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_type = dm.CharField(max_length=16, null=False, blank=False)
    up_last_7d = dm.FloatField(null=True)
    up_last_30d = dm.FloatField(null=True)
    down_last_7d = dm.FloatField(null=True)
    down_last_30d = dm.FloatField(null=True)


class YahooAnalysisGrowthEstimate(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    curr_qtr = dm.FloatField(null=True)
    next_qtr = dm.FloatField(null=True)
    curr_year = dm.FloatField(null=True)
    next_year = dm.FloatField(null=True)
    next_5_years_annum = dm.FloatField(null=True)
    past_5_years_annum = dm.FloatField(null=True)


class YahooHoldersOwnership(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    report_date = dm.DateField(null=False)
    owner_type = dm.CharField(max_length=16, null=False, blank=False)
    organization = dm.CharField(max_length=255, null=False, blank=False)
    pct_held = dm.FloatField(null=False)
    position = dm.FloatField(null=False)
    value = dm.FloatField(null=False)


class YahooHoldersHolders(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    holder_type = dm.CharField(max_length=16, null=False, blank=False)
    name = dm.CharField(max_length=255, null=False, blank=False)
    relation = dm.CharField(max_length=255, blank=True)
    url = dm.CharField(max_length=255, blank=True)
    transaction_description = dm.CharField(max_length=255, blank=True)
    latest_trans_date = dm.DateField(null=True)
    position_direct = dm.FloatField(null=True)
    position_direct_date = dm.DateField(null=True)
    position_indirect = dm.FloatField(null=True)
    position_indirect_date = dm.DateField(null=True)
    position_summary = dm.FloatField(null=True)
    position_summary_date = dm.DateField(null=True)


class YahooHoldersInsiderTransactions(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    filer_name = dm.CharField(max_length=255, null=False, blank=False)
    transaction_text = dm.TextField(blank=True)
    money_text = dm.TextField(blank=True)
    ownership = dm.CharField(max_length=255, blank=True)
    start_date = dm.DateField(null=False)
    value = dm.FloatField(null=False)
    filer_relation = dm.CharField(max_length=255, blank=True)
    shares = dm.FloatField(null=False)
    filer_url = dm.CharField(max_length=255, blank=True)


class YahooHoldersNetSharePurchaseActivity(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    period = dm.CharField(max_length=255, null=False, blank=False)
    net_percent_insider_shares = dm.FloatField(null=True)
    net_info_count = dm.FloatField(null=True)
    net_info_shares = dm.FloatField(null=True)
    buy_percent_insider_shares = dm.FloatField(null=True)
    buy_info_count = dm.FloatField(null=True)
    buy_info_shares = dm.FloatField(null=True)
    sell_percent_insider_shares = dm.FloatField(null=True)
    sell_info_count = dm.FloatField(null=True)
    sell_info_shares = dm.FloatField(null=True)
    total_insider_shares = dm.FloatField(null=True)


class YahooProfileAssetProfile(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    long_business_company = dm.CharField(max_length=255, null=False, blank=False)
    address1 = dm.TextField(blank=True)
    city = dm.CharField(max_length=64, blank=True)
    state = dm.CharField(max_length=16, blank=True)
    country = dm.CharField(max_length=32, blank=True)
    zip = dm.CharField(max_length=8, blank=True)
    phone = dm.CharField(max_length=16, blank=True)
    website = dm.CharField(max_length=255, blank=True)
    industry_symbol = dm.CharField(max_length=16, blank=True)
    industry = dm.CharField(max_length=255, blank=True)
    sector = dm.CharField(max_length=255, blank=True)
    full_time_employees = dm.IntegerField(null=True)
    governance_epoch_date = dm.DateField(null=True)
    compensation_as_of_epoch_date = dm.DateField(null=True)
    audit_risk = dm.FloatField(null=True)
    compensation_risk = dm.FloatField(null=True)
    share_holder_rights_risk = dm.FloatField(null=True)
    board_risk = dm.FloatField(null=True)
    total_risk = dm.FloatField(null=True)


class YahooProfileCompanyOfficers(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    holder_type = dm.CharField(max_length=16, null=False, blank=False)
    name = dm.CharField(max_length=255, null=False, blank=False)
    title = dm.CharField(max_length=255, blank=True)
    age = dm.IntegerField(null=True)
    year_born = dm.IntegerField(null=True)
    fiscal_year = dm.IntegerField(null=True)
    total_pay = dm.FloatField(null=True)
    exercised_value = dm.FloatField(null=True)
    unexercised_value = dm.FloatField(null=True)


class YahooNews(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    title = dm.CharField(max_length=255, null=False, blank=False)
    pubtime = dm.DateTimeField(null=True)
    publisher = dm.CharField(max_length=255, blank=True)
    summary = dm.TextField(blank=True)
    type = dm.CharField(max_length=64, blank=True)
    url = dm.CharField(max_length=255, blank=True)


class YahooSustainability(DatedModel):

    ref_earnings = dm.ForeignKey('EarningsCalendar', null=False, on_delete=dm.CASCADE)
    alcoholic = dm.NullBooleanField()
    adult = dm.NullBooleanField()
    gambling = dm.NullBooleanField()
    tobacco = dm.NullBooleanField()
    animal_testing = dm.NullBooleanField()
    fur_leather = dm.NullBooleanField()
    controversial_weapons = dm.NullBooleanField()
    small_arms = dm.NullBooleanField()
    catholic = dm.NullBooleanField()
    gmo = dm.NullBooleanField()
    military_contract = dm.NullBooleanField()
    pesticides = dm.NullBooleanField()
    coal = dm.NullBooleanField()
    palm_oil = dm.NullBooleanField()
    nuclear = dm.NullBooleanField()
    peer_count = dm.FloatField(null=True)
    peer_group = dm.CharField(max_length=255, blank=True)
    peer_environment_performance_avg = dm.FloatField(null=True)
    peer_environment_performance_max = dm.FloatField(null=True)
    peer_environment_performance_min = dm.FloatField(null=True)
    peer_esg_score_performance_avg = dm.FloatField(null=True)
    peer_esg_score_performance_max = dm.FloatField(null=True)
    peer_esg_score_performance_min = dm.FloatField(null=True)
    peer_governance_performance_avg = dm.FloatField(null=True)
    peer_governance_performance_max = dm.FloatField(null=True)
    peer_governance_performance_min = dm.FloatField(null=True)
    peer_social_performance_avg = dm.FloatField(null=True)
    peer_social_performance_max = dm.FloatField(null=True)
    peer_social_performance_min = dm.FloatField(null=True)
    peer_high_controversy_performance_avg = dm.FloatField(null=True)
    peer_high_controversy_performance_max = dm.FloatField(null=True)
    peer_high_controversy_performance_min = dm.FloatField(null=True)
    rating_month = dm.IntegerField(null=True)
    rating_year = dm.IntegerField(null=True)
    percentile = dm.FloatField(null=True)
    environment_score = dm.FloatField(null=True)
    environment_percentile = dm.FloatField(null=True)
    esg_performance = dm.CharField(max_length=255, blank=True)
    total_esg = dm.FloatField(null=True)
    governance_score = dm.FloatField(null=True)
    governance_percentile = dm.FloatField(null=True)
    social_score = dm.FloatField(null=True)
    social_percentile = dm.FloatField(null=True)
    highest_controversy = dm.FloatField(null=True)
