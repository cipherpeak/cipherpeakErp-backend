from rest_framework import serializers
from .models import (
    ChartOfAccount, Journal, JournalEntry, BankAccount, BankTransaction,
    BankReconciliation, Budget, BudgetLine, FixedAsset, Receivable, ReceivablePayment,
)


# ===========================================================================
# CHART OF ACCOUNTS SERIALIZER
# ===========================================================================

class ChartOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartOfAccount
        fields = '__all__'


# ===========================================================================
# JOURNAL ENTRY SERIALIZER
# ===========================================================================

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
        extra_kwargs = {'journal': {'required': False}}


# ===========================================================================
# JOURNAL SERIALIZER
# ===========================================================================

class JournalSerializer(serializers.ModelSerializer):
    entries = JournalEntrySerializer(many=True, required=False)

    class Meta:
        model = Journal
        fields = '__all__'


# ===========================================================================
# BANK ACCOUNT SERIALIZER
# ===========================================================================

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


# ===========================================================================
# BANK TRANSACTION SERIALIZER
# ===========================================================================

class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = '__all__'


# ===========================================================================
# BANK RECONCILIATION SERIALIZER
# ===========================================================================

class BankReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankReconciliation
        fields = '__all__'


# ===========================================================================
# BUDGET LINE SERIALIZER
# ===========================================================================

class BudgetLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetLine
        fields = '__all__'
        extra_kwargs = {'budget': {'required': False}}


# ===========================================================================
# BUDGET SERIALIZER
# ===========================================================================

class BudgetSerializer(serializers.ModelSerializer):
    lines = BudgetLineSerializer(many=True, required=False)

    class Meta:
        model = Budget
        fields = '__all__'


# ===========================================================================
# FIXED ASSET SERIALIZER
# ===========================================================================

class FixedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAsset
        fields = '__all__'


# ===========================================================================
# RECEIVABLE PAYMENT SERIALIZER
# ===========================================================================

class ReceivablePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivablePayment
        fields = '__all__'
        extra_kwargs = {'receivable': {'required': False}}


# ===========================================================================
# RECEIVABLE SERIALIZER
# ===========================================================================

class ReceivableSerializer(serializers.ModelSerializer):
    payments = ReceivablePaymentSerializer(many=True, required=False)

    class Meta:
        model = Receivable
        fields = '__all__'
