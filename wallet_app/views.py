from datetime import date
import json
import os
import pandas as pd
from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.db.models.functions.datetime import ExtractMonth, ExtractYear
from dateutil.utils import today
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse

from wallet_app.models import Account, FixedInvestment, Saving, Share, VariableInvestment, MonthlyExpense, Indexes, \
    BuyingList, IncomeDistribution, ToDoList
from random import randint


@login_required
def home(request):
    accounts = Account.objects.all().order_by('pk')
    total_value = sum([account.balance for account in accounts])
    salary = IncomeDistribution.objects.all()
    total_salary = sum([values.amount for values in salary])
    indexes = Indexes.objects.all().order_by('value')
    todo_list = ToDoList.objects.all().order_by('-priority', '-pk')
    todo_list_categories = ToDoList.category.field.choices
    todo_list_priorities = ToDoList.priority.field.choices
    _today = date.today()
    data = {
        'accounts': accounts,
        'total_value': total_value,
        'salary': salary,
        'indexes': indexes,
        'total_salary': total_salary,
        'todo_list': todo_list,
        'todo_list_categories': todo_list_categories,
        'todo_list_priorities': todo_list_priorities,
        'today': _today,
    }
    return render(request, 'home.html', data)


@login_required()
def account_panel(request, account_id):
    account = Account.objects.get(pk=account_id)
    if account.type == 'checking_account':
        buying_account = Account.objects.get(name='Compras')
        buying_list = BuyingList.objects.all()
        start_date = request.GET.get('start_date', (date.today().replace(day=1) - relativedelta(months=6)).strftime("%Y-%m-%d"))
        end_date = request.GET.get('end_date', (date.today().replace(day=1) + relativedelta(months=1) - relativedelta(days=1)).strftime("%Y-%m-%d"))
        category_filter = request.GET.get('category', None)
        actual_balance = sum([x.amount for x in account.wallet_app_monthlyexpense_related.all() if x.paid_date <= today().date()])
        account_transactions = MonthlyExpense.objects.filter(Q(account_id=account_id, paid_date__gte=start_date, paid_date__lte=end_date)).order_by('-paid_date', '-pk')
        if category_filter:
            account_transactions = account_transactions.filter(category=MonthlyExpense.get_category_choice(category_filter))
        category_monthly_amount = account_transactions\
            .annotate(month=ExtractMonth('paid_date'), year=ExtractYear('paid_date'), q_category=F('category'))\
            .values('month', 'year', 'q_category')\
            .order_by('year', 'month')\
            .annotate(total=Sum('amount'))\
            .values('month', 'year', 'q_category', 'total')

        date_range = pd.date_range(start_date, end_date, freq='MS').date

        monthly_control = []
        salary = IncomeDistribution.objects.get(distribution='Despesas Mensais')
        for current_date in date_range:
            goal = salary.amount if not category_filter else 0
            current_month_control = {'date': current_date, 'expense_list': [], 'receipt_list': [], 'goal': goal}
            for category in category_monthly_amount:
                q_category = MonthlyExpense.get_category_choice(category['q_category'])
                if category['month'] == current_date.month and category['year'] == current_date.year:
                    if MonthlyExpense.nature(q_category) == 'receipt':
                        current_month_control['receipt_list'].append({q_category: category['total']})
                    elif MonthlyExpense.nature(q_category) == 'expense':
                        current_month_control['expense_list'].append({q_category: category['total']})
            current_month_control.update({'total_expense': abs(sum([list(x.values())[0] for x in current_month_control['expense_list']]))})
            current_month_control.update({'total_revenue': abs(sum([list(x.values())[0] for x in current_month_control['receipt_list']]))})
            if current_month_control['expense_list'] or current_month_control['receipt_list']:
                monthly_control.append(current_month_control)

        pie_chart_labels = []
        pie_chart_data = []
        pie_chart_color = []
        for category in [choice[0] for choice in MonthlyExpense.category.field.choices]:
            _category = MonthlyExpense.get_category_choice(category)
            if MonthlyExpense.nature(_category) == 'expense':
                _sum = abs(sum([monthly_amount['total'] for monthly_amount in category_monthly_amount if monthly_amount['q_category'] == category]))
                _category = MonthlyExpense.get_category_choice(category)
                pie_chart_labels.append(_category)
                pie_chart_data.append(_sum)
                pie_chart_color.append(f'rgb({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})')

        data = {
            'account': account,
            'account_transactions': account_transactions,
            'actual_balance': actual_balance,
            'start_date': start_date,
            'end_date': end_date,
            'monthly_control': monthly_control,
            'categories': [choice[1] for choice in MonthlyExpense.category.field.choices],
            'category_filter': category_filter,
            'pie_chart_labels': pie_chart_labels,
            'pie_chart_data': pie_chart_data,
            'pie_chart_color': pie_chart_color,
            'buying_account': buying_account,
            'buying_list': buying_list,
        }
        return render(request, 'checking_account_panel.html', data)

    elif account.type == 'fixed_investment_account':
        account_transactions = FixedInvestment.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        data = {
            'account': account,
            'account_transactions': account_transactions
        }
        return render(request, 'fixed_account_panel.html', data)

    elif account.type == 'variable_investment_account':
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

    elif account.type == 'saving_account':
        account_transactions = Saving.objects.filter(account_id=account_id).order_by('-paid_date', '-pk')
        data = {
            'account': account,
            'account_transactions': account_transactions
        }
        return render(request, 'saving_account_panel.html', data)


@login_required
def add_buying_list(request, account_id):
    description = request.GET.get('item_description')
    min_price = request.GET.get('item_min_price')
    max_price = request.GET.get('item_max_price')
    qty = request.GET.get('quantity')
    try:
        with transaction.atomic():
            for x in qty:
                BuyingList.objects.create(description=description, min_price=min_price, max_price=max_price)
    except:
        pass
    return redirect(reverse('account_panel', kwargs={'account_id': account_id}))


@login_required
def edit_buying_list(request, account_id, item_id):
    item = get_object_or_404(BuyingList, pk=item_id)
    try:
        with transaction.atomic():
            item.description = request.GET.get('item_description')
            item.min_price = request.GET.get('item_min_price')
            item.max_price = request.GET.get('item_max_price')
            item.save()
    except:
        pass
    return redirect(reverse('account_panel', kwargs={'account_id': account_id}))


@login_required
def delete_buying_list(request, account_id, item_id):
    item = get_object_or_404(BuyingList, pk=item_id)
    item.delete()
    return redirect(reverse('account_panel', kwargs={'account_id': account_id}))


@login_required
def add_todo_list(request):
    item = request.POST.get('item')
    category = request.POST.get('category')
    priority = request.POST.get('priority')
    ToDoList.objects.create(item=item, category=category, priority=priority)
    return redirect(reverse('home'))


@login_required
def delete_todo_list(request, item_id):
    item = ToDoList.objects.get(pk=item_id)
    item.delete()
    return redirect(reverse('home'))


@login_required
def edit_todo_list(request, item_id):
    item = ToDoList.objects.get(pk=item_id)
    item.item = request.POST.get('item')
    item.category = request.POST.get('category')
    item.priority = request.POST.get('priority')
    item.save()
    return redirect(reverse('home'))
