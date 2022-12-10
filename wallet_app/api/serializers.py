from rest_framework import serializers
from wallet_app.models import Account, Share, Saving, FixedInvestment, MonthlyExpense, VariableInvestment


class CustomSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'


class FixedInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedInvestment
        fields = '__all__'


class VariableInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableInvestment
        fields = '__all__'


class MonthlyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyExpense
        fields = '__all__'


class AccountSerializer(CustomSerializer):
    fixed_investment = FixedInvestmentSerializer(many=True, read_only=True)
    variable_investment = VariableInvestmentSerializer(many=True, read_only=True)
    saving = SavingSerializer(many=True, read_only=True)
    expense = MonthlyExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = '__all__'
        extra_fields = ['balance']
