from rest_framework import routers
from wallet_app.api.viewsets import AccountViewSet, ShareViewSet, MonthlyExpenseViewSet, SavingViewSet, \
    VariableInvestmentViewSet, FixedInvestmentViewSet

router = routers.DefaultRouter()

router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'shares', ShareViewSet, basename='share')
router.register(r'monthly_expenses', MonthlyExpenseViewSet, basename='expense')
router.register(r'fixed_investments', FixedInvestmentViewSet, basename='fixed')
router.register(r'variable_investments', VariableInvestmentViewSet, basename='variable')
router.register(r'savings', SavingViewSet, basename='saving')

urlpatterns = router.urls
urlpatterns += [
]
