from django.contrib import admin
from .models import Account, AccountType, Transaction, TransactionCategory

admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Transaction)
admin.site.register(TransactionCategory)
