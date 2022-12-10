import pandas as pd
from pprint import pprint
from django.shortcuts import get_object_or_404
from decimal import Decimal
from wallet_app.models import Account, Saving, MonthlyExpense, Share, VariableInvestment, FixedInvestment


def cc_to_database(datapath, account_name):
    data = pd.read_excel(datapath, sheet_name=account_name)
    json_data = data.to_dict(orient='records')
    account = get_object_or_404(Account, name=account_name)
    for i in range(data.index.stop):
        date = None if pd.isnull(json_data[i]['Data']) else json_data[i]['Data']
        if json_data[i]['Categoria'] == 'Salário':
            category = 'Recebimentos'
        elif json_data[i]['Categoria'] == 'Aula':
            category = 'Estudo'
        elif pd.isnull(json_data[i]['Categoria']):
            category = 'Outros'
        else:
            category = json_data[i]['Categoria']

        name = 'Não especificado' if pd.isnull(json_data[i]['Lançamento']) else json_data[i]['Lançamento']
        amount = 0 if pd.isnull(json_data[i]['Valor Total']) else json_data[i]['Valor Total']
        amount = round(Decimal(amount), 2)
        pandas_dict = {
            'account_id': account.id,
            'paid_date': date,
            'name': name,
            'category': category,
            'amount': amount,
            'balance': account.balance + amount
        }
        try:
            me = MonthlyExpense.objects.get(name=name, category=category, paid_date=date, amount=amount)
        except:
            me = MonthlyExpense(**pandas_dict)
            me.save()
            pprint(f'object saved successfully: {pandas_dict}')


def reserva_to_database(datapath, account_name):
    data = pd.read_excel(datapath, sheet_name=account_name)
    json_data = data.to_dict(orient='records')
    account = get_object_or_404(Account, name=account_name)
    for i in range(data.index.stop):
        date = None if pd.isnull(json_data[i]['Data']) else json_data[i]['Data']
        if json_data[i]['Movimentação'] == 'Salário':
            category = 'Depósito'
        elif json_data[i]['Movimentação'] == 'Empréstimo':
            category = 'Depósito'
        else:
            category = json_data[i]['Movimentação']

        amount = 0 if pd.isnull(json_data[i]['Valor']) else json_data[i]['Valor']
        pandas_dict = {
            'account_id': account.id,
            'paid_date': date,
            'category': category,
            'amount': round(Decimal(amount), 2)
        }
        try:
            me = Saving.objects.get(category=category, paid_date=date, amount=pandas_dict['amount'])
        except:
            me = Saving(**pandas_dict)
            me.save()
            pprint(f'object saved successfully: {pandas_dict}')


def variable_to_database(datapath, account_name):
    data = pd.read_excel(datapath, sheet_name=account_name)
    json_data = data.to_dict(orient='records')
    account = get_object_or_404(Account, name=account_name)
    for i in range(data.index.stop):
        name = json_data[i]['Cota']
        try:
            share = Share.objects.get(name=name)
            share_id = share.id
        except:
            share = Share.objects.create(name=name)
            share_id = share.id

        date = None if pd.isnull(json_data[i]['Data']) else json_data[i]['Data']
        amount = 0 if pd.isnull(json_data[i]['Valor']) else json_data[i]['Valor']
        quantity = 0 if pd.isnull(json_data[i]['Número de Cotas']) else json_data[i]['Número de Cotas']
        pandas_dict = {
            'account_id': account.id,
            'share_id': share_id,
            'paid_date': date,
            'amount': round(Decimal(amount), 2),
            'number_of_shares': quantity
        }
        try:
            me = VariableInvestment.objects.get(share_id=share_id, paid_date=date, amount=pandas_dict['amount'],
                                                number_of_shares=quantity)
        except:
            me = VariableInvestment(**pandas_dict)
            me.save()
            pprint(f'object saved successfully: {pandas_dict}')


def fixed_to_database(datapath, account_name):
    data = pd.read_excel(datapath, sheet_name=account_name)
    json_data = data.to_dict(orient='records')
    account = get_object_or_404(Account, name=account_name)
    for i in range(data.index.stop):
        date = None if pd.isnull(json_data[i]['Aplicação']) else json_data[i]['Aplicação']
        due_date = None if pd.isnull(json_data[i]['Vencimento']) else json_data[i]['Vencimento']
        amount = 0 if pd.isnull(json_data[i]['Valor Inicial']) else json_data[i]['Valor Inicial']
        projected_value = 0 if pd.isnull(json_data[i]['Valor Projetado']) else json_data[i]['Valor Projetado']
        profitability = 0 if pd.isnull(json_data[i]['Rentabilidade']) else json_data[i]['Rentabilidade']
        category = None if pd.isnull(json_data[i]['Categoria']) else json_data[i]['Categoria']
        pandas_dict = {
            'account_id': account.id,
            'due_date': due_date,
            'paid_date': date,
            'amount': round(Decimal(amount), 2),
            'projected_value': projected_value,
            'profitability': profitability,
            'category': category
        }
        try:
            me = FixedInvestment.objects.get(account_id=account.id, paid_date=date, due_date=due_date,
                                             amount=pandas_dict['amount'],
                                             category=category, profitability=profitability)
        except:
            me = FixedInvestment(**pandas_dict)
            me.save()
            pprint(f'object saved successfully: {pandas_dict}')
