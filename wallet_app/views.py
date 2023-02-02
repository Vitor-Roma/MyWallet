import json
import os
from datetime import date
from django.db.models import Count, Sum, F
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
        actual_balance = sum([x.amount if x.paid_date <= today().date() else 0 for x in account.wallet_app_monthlyexpense_related.all()])
        account_transactions = MonthlyExpense.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        category_monthly_amount = [x for x in MonthlyExpense.objects.filter(account_id=account_id
                                                          ).annotate(month=ExtractMonth('paid_date'),
                                                          year=ExtractYear('paid_date'),
                                                          q_category=F('category')
                                                          ).values('month', 'year', 'q_category'
                                                          ).order_by('year', 'month'
                                                          ).annotate(total=Sum('amount')
                                                          ).values('month', 'year', 'q_category', 'total')
                                                          ]
        data = {
            'account': account,
            'account_transactions': account_transactions,
            'actual_balance': actual_balance,
            'category_monthly_amount': category_monthly_amount,
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
