from rest_framework import viewsets, permissions
from .serializers import AccountSerializer, ShareSerializer, MonthlyExpenseSerializer, SavingSerializer, \
    FixedInvestmentSerializer, VariableInvestmentSerializer
from wallet_app.models import Account, Share, MonthlyExpense, Saving, FixedInvestment, VariableInvestment


class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class ShareViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShareSerializer
    queryset = Share.objects.all()


class MonthlyExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = MonthlyExpenseSerializer
    queryset = MonthlyExpense.objects.all()


class SavingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()


class FixedInvestmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = FixedInvestmentSerializer
    queryset = FixedInvestment.objects.all()


class VariableInvestmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = VariableInvestmentSerializer
    queryset = VariableInvestment.objects.all()
