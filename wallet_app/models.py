from django.db import models


class Account(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True, null=False, blank=False)
    type = models.CharField('Tipo de conta', max_length=50, choices=[
        ('checking_account', 'Conta Corrente'),
        ('fixed_investment_account', 'Investimento renda fixa'),
        ('variable_investment_account', 'Investimento renda variável'),
        ('saving_account', 'Reservas'),
    ])
    description = models.CharField('Descrição', max_length=999, default=None, null=True, blank=True)
    color = models.CharField('Cor', max_length=100, default='White', null=False, blank=False)

    def __str__(self):
        return self.name

    @property
    def balance(self):
        monthlyexpense_sum = sum([x.amount for x in self.wallet_app_monthlyexpense_related.all()])
        fixedinvestment_sum = sum([x.amount for x in self.wallet_app_fixedinvestment_related.all()])
        variableinvestment_sum = sum(
            [x.amount * x.number_of_shares for x in self.wallet_app_variableinvestment_related.all()])
        saving_sum = sum([x.amount for x in self.wallet_app_saving_related.all()])
        balance = sum([monthlyexpense_sum, fixedinvestment_sum, variableinvestment_sum, saving_sum])
        return balance


class BaseTransaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT, null=False,
                                blank=False, related_name="%(app_label)s_%(class)s_related",
                                related_query_name="%(app_label)s_%(class)ss")
    paid_date = models.DateField("Data do pagamento", null=True, blank=True)
    amount = models.DecimalField('Valor', max_digits=20, decimal_places=2)

    class Meta:
        abstract = True


class Share(models.Model):
    name = models.CharField('Cota', max_length=100, unique=True, null=False, blank=False)
    description = models.TextField('Descrição', null=True, blank=True)
    current_value = models.DecimalField('Valor atual da cota', null=True, blank=True, max_digits=10, decimal_places=2)
    type = models.CharField('Tipo de ação', max_length=50, default=None, choices=[
        ('fiss', 'Fiis'),
        ('capital_shares', 'Ações'),
    ])

    def __str__(self):
        return self.name


class Saving(BaseTransaction):
    category = models.CharField('Categoria', max_length=50, unique=False, choices=[
        ('deposit', "Depósito"),
        ('revenue', 'Rendimentos'),
        ('loss', 'Retirada'),
        ('Other', 'Outro')
    ])


class FixedInvestment(BaseTransaction):
    projected_value = models.DecimalField('Valor Projetado', null=True, blank=True, max_digits=10, decimal_places=2)
    due_date = models.DateField('Vencimento')
    profitability = models.FloatField('Rentabilidade', null=False, blank=False)
    category = models.CharField('Categoria', max_length=50, unique=False, blank=False, null=False, choices=[
        ('cdb', 'CDB'),
        ('lci', 'LCI'),
        ('lca', 'LCA'),
        ('tesouro_ipca', 'Tesouro IPCA'),
        ('tesouro_selic', 'Tesouro Selic'),
        ('tesouro_prefix', 'Tesouro Prefixado'),
    ])
    obs = models.CharField('Observações', max_length=500, blank=True, null=True)
    link = models.CharField('Link', max_length=200, blank=True, null=True)


class VariableInvestment(BaseTransaction):
    share = models.ForeignKey(Share, on_delete=models.PROTECT, related_name='share_transaction')
    number_of_shares = models.IntegerField('Número de cotas', default=1, null=False, blank=False)

    @property
    def total_value(self):
        return self.amount * self.number_of_shares

    @property
    def balance(self):
        return sum([self.balance - x.current_value for x in self.share_transaction.all()])


class MonthlyExpense(BaseTransaction):
    name = models.CharField('Nome', max_length=200, unique=False, null=False, blank=False)
    balance = models.DecimalField('Saldo', null=True, blank=True, max_digits=50, decimal_places=2)
    category = models.CharField('Categoria', max_length=100, blank=False, null=False, choices=[
        ('receipts', 'Recebimentos'),
        ('purchases', 'Compras'),
        ('credit_card', 'Cartão'),
        ('yield', 'Rendimentos'),
        ('refund', 'Reembolso'),
        ('dwelling', 'Moradias'),
        ('pharmacy', 'Farmácia'),
        ('bills', 'Contas'),
        ('grocery', 'Mercado'),
        ('food', 'Alimentação'),
        ('travel', 'Viagem'),
        ('health', 'Saúde'),
        ('study', 'Estudo'),
        ('mother', 'Mãe'),
        ('transport', 'Transporte'),
        ('game', 'Jogo'),
        ('leisure', 'Lazer'),
        ('pet', 'Pet'),
        ('balance', 'Saldo +/-'),
        ('others', 'Outros'),
    ])

    @property
    def date(self):
        return f'{self.paid_date.day}/{self.paid_date.month}/{self.paid_date.year}' if self.paid_date else self.paid_date

    def __str__(self):
        return f' {self.date} {self.name} R$: {self.amount}'
