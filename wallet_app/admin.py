from django.contrib import admin
from .models import Account, Saving, MonthlyExpense, FixedInvestment, VariableInvestment, Share, Indexes, BuyingList, ToDoList, Income, IncomeDistribution, NetWorth

admin.site.register(Account)
admin.site.register(Saving)
admin.site.register(MonthlyExpense)
admin.site.register(FixedInvestment)
admin.site.register(VariableInvestment)
admin.site.register(Share)
admin.site.register(Indexes)
admin.site.register(BuyingList)
admin.site.register(ToDoList)
admin.site.register(Income)
admin.site.register(IncomeDistribution)
admin.site.register(NetWorth)
