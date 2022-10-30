from django.db import models


class AccountType(models.Model):
    type = models.CharField('Tipo de conta', max_length=50, unique=True, choices=[
        ('checking_account', 'Conta Corrente'),
        ('fixed_investment_account', 'Investimento renda fixa'),
        ('variable_investment_account', 'Investimento renda variável'),
        ('saving_account', 'Reservas'),
    ])


class TransactionCategory(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True)


class Account(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True)
    initial_value = models.DecimalField("Valor Inicial", max_digits=10, decimal_places=2)
    balance = models.DecimalField("Saldo", max_digits=10, decimal_places=2)
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='account_type')
    description = models.CharField('Descrição', max_length=999)


class Transaction(models.Model):
    name = models.CharField('Nome', max_length=100)
    date = models.DateField('Data de Pagamento', blank=True, null=True)
    category = models.ForeignKey(TransactionCategory, on_delete=models.PROTECT, related_name='transaction_category')
    amount = models.DecimalField("Valor", max_digits=10, decimal_places=2)


