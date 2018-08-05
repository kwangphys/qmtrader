# Generated by Django 2.0.6 on 2018-08-05 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yahoo', '0003_auto_20180627_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='YahooAnalysisEarningsEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_type', models.CharField(max_length=16)),
                ('n_analysts', models.IntegerField()),
                ('avg', models.FloatField(null=True)),
                ('low', models.FloatField(null=True)),
                ('high', models.FloatField(null=True)),
                ('year_ago_eps', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooAnalysisEarningsHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_type', models.CharField(max_length=16)),
                ('eps_est', models.FloatField(null=True)),
                ('eps_actual', models.FloatField(null=True)),
                ('eps_diff', models.FloatField(null=True)),
                ('surprise', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooAnalysisEPSRevisions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_type', models.CharField(max_length=16)),
                ('up_last_7d', models.FloatField(null=True)),
                ('up_last_30d', models.FloatField(null=True)),
                ('down_last_7d', models.FloatField(null=True)),
                ('down_last_30d', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooAnalysisEPSTrend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_type', models.CharField(max_length=16)),
                ('eps_curr', models.FloatField(null=True)),
                ('eps_7d', models.FloatField(null=True)),
                ('eps_30d', models.FloatField(null=True)),
                ('eps_60d', models.FloatField(null=True)),
                ('eps_90d', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooAnalysisGrowthEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('curr_qtr', models.FloatField(null=True)),
                ('next_qtr', models.FloatField(null=True)),
                ('curr_year', models.FloatField(null=True)),
                ('next_year', models.FloatField(null=True)),
                ('next_5_years_annum', models.FloatField(null=True)),
                ('past_5_years_annum', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooAnalysisRevenueEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_type', models.CharField(max_length=16)),
                ('n_analysts', models.IntegerField()),
                ('avg', models.FloatField(null=True)),
                ('low', models.FloatField(null=True)),
                ('high', models.FloatField(null=True)),
                ('year_ago_sales', models.FloatField(null=True)),
                ('sales_growth', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooFinancialsBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_date', models.DateField()),
                ('report_freq', models.CharField(choices=[('q', 'Quarterly'), ('a', 'Annual')], max_length=1)),
                ('cash', models.FloatField(null=True)),
                ('short_term_investments', models.FloatField(null=True)),
                ('net_receivables', models.FloatField(null=True)),
                ('inventory', models.FloatField(null=True)),
                ('other_current_assets', models.FloatField(null=True)),
                ('total_current_assets', models.FloatField()),
                ('long_term_investments', models.FloatField(null=True)),
                ('property_plant_equipment', models.FloatField(null=True)),
                ('good_will', models.FloatField(null=True)),
                ('intangible_assets', models.FloatField(null=True)),
                ('accumulated_amortization', models.FloatField(null=True)),
                ('other_assets', models.FloatField(null=True)),
                ('deferred_long_term_assets', models.FloatField(null=True)),
                ('total_assets', models.FloatField()),
                ('account_payable', models.FloatField(null=True)),
                ('short_long_term_debt', models.FloatField(null=True)),
                ('other_current_liab', models.FloatField(null=True)),
                ('total_current_liabilities', models.FloatField()),
                ('long_term_debt', models.FloatField(null=True)),
                ('other_liab', models.FloatField(null=True)),
                ('deferred_long_term_liab', models.FloatField(null=True)),
                ('minority_interest', models.FloatField(null=True)),
                ('negative_good_will', models.FloatField(null=True)),
                ('total_liab', models.FloatField()),
                ('stock_option_warrants', models.FloatField(null=True)),
                ('redeemable_preferred_stock', models.FloatField(null=True)),
                ('preferred_stock', models.FloatField(null=True)),
                ('common_stock', models.FloatField(null=True)),
                ('retained_earnings', models.FloatField(null=True)),
                ('treasury_stock', models.FloatField(null=True)),
                ('capital_surplus', models.FloatField(null=True)),
                ('other_stockholder_equity', models.FloatField(null=True)),
                ('total_stockholder_equity', models.FloatField(null=True)),
                ('net_tangible_assets', models.FloatField()),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooFinancialsCashflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_date', models.DateField()),
                ('report_freq', models.CharField(choices=[('q', 'Quarterly'), ('a', 'Annual')], max_length=1)),
                ('net_income', models.FloatField(null=True)),
                ('depreciation', models.FloatField(null=True)),
                ('change_to_netincome', models.FloatField(null=True)),
                ('change_to_account_receivables', models.FloatField(null=True)),
                ('change_to_liabilities', models.FloatField(null=True)),
                ('change_to_inventory', models.FloatField(null=True)),
                ('change_to_operating_activities', models.FloatField(null=True)),
                ('total_cash_from_operating_activities', models.FloatField()),
                ('capital_expenditures', models.FloatField(null=True)),
                ('investments', models.FloatField(null=True)),
                ('other_cashflows_from_investing_activities', models.FloatField(null=True)),
                ('total_cashflows_from_investing_activities', models.FloatField()),
                ('dividend_paid', models.FloatField(null=True)),
                ('sale_purchase_of_stock', models.FloatField(null=True)),
                ('net_borrowings', models.FloatField(null=True)),
                ('other_cashflows_from_financing_activities', models.FloatField(null=True)),
                ('total_cash_from_financing_activities', models.FloatField()),
                ('effect_of_exchange_rate', models.FloatField(null=True)),
                ('change_in_cash', models.FloatField()),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooFinancialsIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_date', models.DateField()),
                ('report_freq', models.CharField(choices=[('q', 'Quarterly'), ('a', 'Annual')], max_length=1)),
                ('total_revenue', models.FloatField()),
                ('cost_of_revenue', models.FloatField(null=True)),
                ('gross_profit', models.FloatField()),
                ('research_development', models.FloatField(null=True)),
                ('selling_general_administrative', models.FloatField(null=True)),
                ('non_recurring', models.FloatField(null=True)),
                ('other_operating_expenses', models.FloatField(null=True)),
                ('total_operating_expenses', models.FloatField(null=True)),
                ('operating_income', models.FloatField()),
                ('total_other_income_expense_net', models.FloatField(null=True)),
                ('ebit', models.FloatField(null=True)),
                ('interest_expense', models.FloatField(null=True)),
                ('income_before_tax', models.FloatField(null=True)),
                ('income_tax_expense', models.FloatField(null=True)),
                ('minority_interest', models.FloatField(null=True)),
                ('net_income_from_continuing_ops', models.FloatField()),
                ('discontinued_operations', models.FloatField(null=True)),
                ('extradinary_items', models.FloatField(null=True)),
                ('effect_of_accounting_changes', models.FloatField(null=True)),
                ('other_items', models.FloatField(null=True)),
                ('net_income', models.FloatField()),
                ('preferred_stock_and_other_adjustments', models.FloatField(null=True)),
                ('net_income_applicable_to_common_shares', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooHoldersHolders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('holder_type', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=255)),
                ('relation', models.CharField(blank=True, max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('transaction_description', models.CharField(blank=True, max_length=255)),
                ('latest_trans_date', models.DateField(null=True)),
                ('position_direct', models.FloatField(null=True)),
                ('position_direct_date', models.DateField(null=True)),
                ('position_indirect', models.FloatField(null=True)),
                ('position_indirect_date', models.DateField(null=True)),
                ('position_summary', models.FloatField(null=True)),
                ('position_summary_date', models.DateField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooHoldersInsiderTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('filer_name', models.CharField(max_length=255)),
                ('transaction_text', models.TextField(blank=True)),
                ('money_text', models.TextField(blank=True)),
                ('ownership', models.CharField(blank=True, max_length=255)),
                ('start_date', models.DateField()),
                ('value', models.FloatField()),
                ('filer_relation', models.CharField(blank=True, max_length=255)),
                ('shares', models.FloatField()),
                ('filer_url', models.CharField(blank=True, max_length=255)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooHoldersNetSharePurchaseActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('period', models.CharField(max_length=255)),
                ('net_percent_insider_shares', models.FloatField(null=True)),
                ('net_info_count', models.FloatField(null=True)),
                ('net_info_shares', models.FloatField(null=True)),
                ('buy_percent_insider_shares', models.FloatField(null=True)),
                ('buy_info_count', models.FloatField(null=True)),
                ('buy_info_shares', models.FloatField(null=True)),
                ('sell_percent_insider_shares', models.FloatField(null=True)),
                ('sell_info_count', models.FloatField(null=True)),
                ('sell_info_shares', models.FloatField(null=True)),
                ('total_insider_shares', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooHoldersOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('report_date', models.DateField()),
                ('owner_type', models.CharField(max_length=16)),
                ('organization', models.CharField(max_length=255)),
                ('pct_held', models.FloatField()),
                ('position', models.FloatField()),
                ('value', models.FloatField()),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('title', models.CharField(max_length=255)),
                ('pubtime', models.DateTimeField(null=True)),
                ('publisher', models.CharField(blank=True, max_length=255)),
                ('summary', models.TextField(blank=True)),
                ('type', models.CharField(blank=True, max_length=64)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooProfileAssetProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('long_business_company', models.CharField(max_length=255)),
                ('address1', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=64)),
                ('state', models.CharField(blank=True, max_length=16)),
                ('country', models.CharField(blank=True, max_length=32)),
                ('zip', models.CharField(blank=True, max_length=8)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('website', models.CharField(blank=True, max_length=255)),
                ('industry_symbol', models.CharField(blank=True, max_length=16)),
                ('industry', models.CharField(blank=True, max_length=255)),
                ('sector', models.CharField(blank=True, max_length=255)),
                ('full_time_employees', models.IntegerField(null=True)),
                ('governance_epoch_date', models.DateField(null=True)),
                ('compensation_as_of_epoch_date', models.DateField(null=True)),
                ('audit_risk', models.FloatField(null=True)),
                ('compensation_risk', models.FloatField(null=True)),
                ('share_holder_rights_risk', models.FloatField(null=True)),
                ('board_risk', models.FloatField(null=True)),
                ('total_risk', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooProfileCompanyOfficers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('holder_type', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('age', models.IntegerField(null=True)),
                ('year_born', models.IntegerField(null=True)),
                ('fiscal_year', models.IntegerField(null=True)),
                ('total_pay', models.FloatField(null=True)),
                ('exercised_value', models.FloatField(null=True)),
                ('unexercised_value', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('market_cap_intraday', models.FloatField()),
                ('enterprise_value', models.FloatField()),
                ('trailing_pe_ratio', models.FloatField(null=True)),
                ('forward_pe_ratio', models.FloatField(null=True)),
                ('peg_ratio_5y_expected', models.FloatField()),
                ('price_sales_ratio', models.FloatField()),
                ('price_book_ratio', models.FloatField()),
                ('value_revenue_ratio', models.FloatField()),
                ('value_ebitda_ratio', models.FloatField()),
                ('beta', models.FloatField()),
                ('week52_change', models.FloatField()),
                ('week52_high', models.FloatField()),
                ('week52_low', models.FloatField()),
                ('day50_moving_average', models.FloatField()),
                ('day200_moving_average', models.FloatField()),
                ('fiscal_year_ends', models.DateField()),
                ('most_recent_quarter', models.DateField()),
                ('profit_margin', models.FloatField()),
                ('operating_margin', models.FloatField()),
                ('return_on_assets', models.FloatField()),
                ('return_on_equity', models.FloatField()),
                ('revenue', models.FloatField()),
                ('revenue_per_share', models.FloatField()),
                ('quarterly_revenue_growth', models.FloatField()),
                ('gross_profit', models.FloatField()),
                ('ebitda', models.FloatField()),
                ('net_income_avi_to_common', models.FloatField()),
                ('diluted_eps', models.FloatField()),
                ('quarterly_earnings_growth', models.FloatField(null=True)),
                ('total_cash', models.FloatField()),
                ('total_cash_per_share', models.FloatField()),
                ('total_debt', models.FloatField()),
                ('total_debt_to_equity', models.FloatField()),
                ('current_ratio', models.FloatField()),
                ('book_value_per_share', models.FloatField()),
                ('operating_cash_flow', models.FloatField()),
                ('levered_free_cash_flow', models.FloatField()),
                ('avg_vol_3m', models.FloatField()),
                ('avg_vol_10d', models.FloatField()),
                ('shares_outstanding', models.FloatField()),
                ('shares_float', models.FloatField()),
                ('insider_hold_ratio', models.FloatField()),
                ('institutions_hold_ratio', models.FloatField()),
                ('shares_short', models.FloatField()),
                ('short_ratio', models.FloatField()),
                ('short_to_float_ratio', models.FloatField()),
                ('shares_short_prev_month', models.FloatField()),
                ('forward_annual_dividend_rate', models.FloatField(null=True)),
                ('forward_annual_dividend_yield', models.FloatField(null=True)),
                ('trailing_annual_dividend_rate', models.FloatField(null=True)),
                ('trailing_annual_dividend_yield', models.FloatField(null=True)),
                ('average_dividend_yield_5y', models.FloatField(null=True)),
                ('payout_ratio', models.FloatField()),
                ('dividend_date', models.DateField(null=True)),
                ('ex_dividend_date', models.DateField(null=True)),
                ('last_split_factor', models.FloatField(null=True)),
                ('last_split_date', models.DateField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YahooSustainability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('alcoholic', models.NullBooleanField()),
                ('adult', models.NullBooleanField()),
                ('gambling', models.NullBooleanField()),
                ('tobacco', models.NullBooleanField()),
                ('animal_testing', models.NullBooleanField()),
                ('fur_leather', models.NullBooleanField()),
                ('controversial_weapons', models.NullBooleanField()),
                ('small_arms', models.NullBooleanField()),
                ('catholic', models.NullBooleanField()),
                ('gmo', models.NullBooleanField()),
                ('military_contract', models.NullBooleanField()),
                ('pesticides', models.NullBooleanField()),
                ('coal', models.NullBooleanField()),
                ('palm_oil', models.NullBooleanField()),
                ('nuclear', models.NullBooleanField()),
                ('peer_count', models.FloatField(null=True)),
                ('peer_group', models.CharField(blank=True, max_length=255)),
                ('peer_environment_performance_avg', models.FloatField(null=True)),
                ('peer_environment_performance_max', models.FloatField(null=True)),
                ('peer_environment_performance_min', models.FloatField(null=True)),
                ('peer_esg_score_performance_avg', models.FloatField(null=True)),
                ('peer_esg_score_performance_max', models.FloatField(null=True)),
                ('peer_esg_score_performance_min', models.FloatField(null=True)),
                ('peer_governance_performance_avg', models.FloatField(null=True)),
                ('peer_governance_performance_max', models.FloatField(null=True)),
                ('peer_governance_performance_min', models.FloatField(null=True)),
                ('peer_social_performance_avg', models.FloatField(null=True)),
                ('peer_social_performance_max', models.FloatField(null=True)),
                ('peer_social_performance_min', models.FloatField(null=True)),
                ('peer_high_controversy_performance_avg', models.FloatField(null=True)),
                ('peer_high_controversy_performance_max', models.FloatField(null=True)),
                ('peer_high_controversy_performance_min', models.FloatField(null=True)),
                ('rating_month', models.IntegerField(null=True)),
                ('rating_year', models.IntegerField(null=True)),
                ('percentile', models.FloatField(null=True)),
                ('environment_score', models.FloatField(null=True)),
                ('environment_percentile', models.FloatField(null=True)),
                ('esg_performance', models.CharField(blank=True, max_length=255)),
                ('total_esg', models.FloatField(null=True)),
                ('governance_score', models.FloatField(null=True)),
                ('governance_percentile', models.FloatField(null=True)),
                ('social_score', models.FloatField(null=True)),
                ('social_percentile', models.FloatField(null=True)),
                ('highest_controversy', models.FloatField(null=True)),
                ('ref_earnings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yahoo.EarningsCalendar')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
