import datetime
import json
import os

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F
from django.db.models.functions.datetime import ExtractMonth, ExtractYear
from dateutil.utils import today
from django.shortcuts import render
from wallet_app.models import Account, FixedInvestment, Saving, Share, VariableInvestment, MonthlyExpense, Indexes


def home(request):
    accounts = Account.objects.all().order_by('pk')
    total_value = sum([account.balance for account in accounts])
    salary = json.loads(os.environ.get('SALARY').replace("'", '"'))
    salary['Total'] = sum(salary.values())
    indexes = Indexes.objects.all().order_by('value')
    data = {
        'accounts': accounts,
        'total_value': total_value,
        'salary': salary,
        'indexes': indexes,
    }
    return render(request, 'home.html', data)


def account_panel(request, account_id, account_type):
    account = Account.objects.get(pk=account_id)
    if account.type == 'checking_account':
        actual_balance = sum([x.amount for x in account.wallet_app_monthlyexpense_related.all() if x.paid_date <= today().date()])
        account_transactions = MonthlyExpense.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        category_monthly_amount = MonthlyExpense.objects\
            .filter(account_id=account_id)\
            .annotate(month=ExtractMonth('paid_date'), year=ExtractYear('paid_date'), q_category=F('category'))\
            .values('month', 'year', 'q_category')\
            .order_by('year', 'month')\
            .annotate(total=Sum('amount'))\
            .values('month', 'year', 'q_category', 'total')

        selected_date = today() - relativedelta(months=1)
        first_date_month, last_date_month = category_monthly_amount.first()['month'], category_monthly_amount.last()['month']
        first_date_year, last_date_year = category_monthly_amount.first()['year'], category_monthly_amount.last()['year']
        fist_date, last_date = datetime.datetime(first_date_year, first_date_month, day=1), datetime.datetime(last_date_year, last_date_month, day=1)
        date_range = pd.date_range(fist_date, last_date, freq='MS').to_pydatetime()

        monthly_control = []
        for current_date in date_range:
            current_month_control = {'date': current_date, 'expense_list': [], 'revenue_list': []}
            for category in category_monthly_amount:
                q_category = MonthlyExpense.get_category_choice(category['q_category'])
                if category['month'] == current_date.month and category['year'] == current_date.year:
                    if MonthlyExpense.is_revenue(q_category):
                        current_month_control['revenue_list'].append({q_category: category['total']})
                    else:
                        current_month_control['expense_list'].append({q_category: category['total']})
            current_month_control.update({'total_expense': sum([list(x.values())[0] for x in current_month_control['expense_list']])})
            current_month_control.update({'total_revenue': sum([list(x.values())[0] for x in current_month_control['revenue_list']])})
            if current_month_control['expense_list'] or current_month_control['revenue_list']:
                monthly_control.append(current_month_control)

        total_per_month = sum([amount['total'] for amount in category_monthly_amount if amount['month'] == selected_date.month and amount['year'] == selected_date.year])
        data = {
            'account': account,
            'account_transactions': account_transactions,
            'actual_balance': actual_balance,
            'monthly_control': monthly_control,
            'selected_date': selected_date,
            'total_per_month': total_per_month,
        }
        return render(request, 'checking_account_panel.html', data)

    elif account_type == 'fixed_investment_account':
        account_transactions = FixedInvestment.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        data = {
            'account': account,
            'account_transactions': account_transactions
        }
        return render(request, 'fixed_account_panel.html', data)

    elif account_type == 'variable_investment_account':
        account_transactions = VariableInvestment.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        shares = Share.objects.all()
        paid_value_per_share = {share.name: sum(
            [transaction.number_of_shares * transaction.amount for transaction in account_transactions if
             transaction.share.name == share.name]) for share in shares}

        current_value_per_share = {share.name: sum([account.number_of_shares for account in account_transactions if
                                                    account.share.name == share.name]) * share.current_value for share in shares}

        total_current_value = sum([current_value_per_share[share.name] for share in shares])
        balance_per_share = {share.name: current_value_per_share[share.name] - paid_value_per_share[share.name] for share in shares}
        data = {
            'account': account,
            'account_transactions': account_transactions,
            'paid_value_per_share': paid_value_per_share,
            'current_value_per_share': current_value_per_share,
            'current_value': total_current_value,
            'balance_per_share': balance_per_share,
            'shares': shares
        }
        return render(request, 'variable_account_panel.html', data)

    elif account_type == 'saving_account':
        account_transactions = Saving.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        data = {
            'account': account,
            'account_transactions': account_transactions
        }
        return render(request, 'saving_account_panel.html', data)
