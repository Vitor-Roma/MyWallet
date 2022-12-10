from django.contrib import admin
from .models import Account, Saving, MonthlyExpense, FixedInvestment, VariableInvestment, Share

admin.site.register(Account)
admin.site.register(Saving)
admin.site.register(MonthlyExpense)
admin.site.register(FixedInvestment)
admin.site.register(VariableInvestment)
admin.site.register(Share)
