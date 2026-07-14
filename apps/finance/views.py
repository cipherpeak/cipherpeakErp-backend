from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    ChartOfAccount, Journal, BankAccount, BankTransaction,
    BankReconciliation, Budget, FixedAsset, Receivable,
)
from .serializers import (
    ChartOfAccountSerializer, JournalSerializer, BankAccountSerializer,
    BankTransactionSerializer, BankReconciliationSerializer, BudgetSerializer,
    FixedAssetSerializer, ReceivableSerializer,
)
from . import services


# ===========================================================================
# CHART OF ACCOUNTS VIEWSET
# ===========================================================================

class ChartOfAccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        accounts = services.get_all_accounts()
        serializer = ChartOfAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        account = get_object_or_404(ChartOfAccount, pk=pk)
        serializer = ChartOfAccountSerializer(account)
        return Response(serializer.data)

    def create(self, request):
        serializer = ChartOfAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_account(serializer.validated_data)
            return Response({"message": "Account created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        account = get_object_or_404(ChartOfAccount, pk=pk)
        serializer = ChartOfAccountSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_account(account, serializer.validated_data)
            return Response({"message": "Account updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        account = get_object_or_404(ChartOfAccount, pk=pk)
        serializer = ChartOfAccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_account(account, serializer.validated_data)
            return Response({"message": "Account updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        account = get_object_or_404(ChartOfAccount, pk=pk)
        services.delete_account(account)
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# JOURNAL VIEWSET
# ===========================================================================

class JournalViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        journals = services.get_all_journals()
        serializer = JournalSerializer(journals, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        journal = services.get_journal_with_entries(pk)
        serializer = JournalSerializer(journal)
        return Response(serializer.data)

    def create(self, request):
        serializer = JournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_journal(serializer.validated_data)
            return Response({"message": "Journal created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        journal = get_object_or_404(Journal, pk=pk)
        serializer = JournalSerializer(journal, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_journal(journal, serializer.validated_data)
            return Response({"message": "Journal updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        journal = get_object_or_404(Journal, pk=pk)
        serializer = JournalSerializer(journal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_journal(journal, serializer.validated_data)
            return Response({"message": "Journal updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        journal = get_object_or_404(Journal, pk=pk)
        services.delete_journal(journal)
        return Response({"message": "Journal deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BANK ACCOUNT VIEWSET
# ===========================================================================

class BankAccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        accounts = services.get_all_bank_accounts()
        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = BankAccountSerializer(account)
        return Response(serializer.data)

    def create(self, request):
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bank_account(serializer.validated_data)
            return Response({"message": "Bank account created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = BankAccountSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bank_account(account, serializer.validated_data)
            return Response({"message": "Bank account updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = BankAccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bank_account(account, serializer.validated_data)
            return Response({"message": "Bank account updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        account = get_object_or_404(BankAccount, pk=pk)
        services.delete_bank_account(account)
        return Response({"message": "Bank account deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BANK TRANSACTION VIEWSET
# ===========================================================================

class BankTransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        txns = services.get_all_bank_transactions()
        serializer = BankTransactionSerializer(txns, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        txn = get_object_or_404(BankTransaction, pk=pk)
        serializer = BankTransactionSerializer(txn)
        return Response(serializer.data)

    def create(self, request):
        serializer = BankTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bank_transaction(serializer.validated_data)
            return Response({"message": "Bank transaction created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        txn = get_object_or_404(BankTransaction, pk=pk)
        serializer = BankTransactionSerializer(txn, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bank_transaction(txn, serializer.validated_data)
            return Response({"message": "Bank transaction updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        txn = get_object_or_404(BankTransaction, pk=pk)
        serializer = BankTransactionSerializer(txn, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bank_transaction(txn, serializer.validated_data)
            return Response({"message": "Bank transaction updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        txn = get_object_or_404(BankTransaction, pk=pk)
        services.delete_bank_transaction(txn)
        return Response({"message": "Bank transaction deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BANK RECONCILIATION VIEWSET
# ===========================================================================

class BankReconciliationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        recs = services.get_all_bank_reconciliations()
        serializer = BankReconciliationSerializer(recs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        rec = get_object_or_404(BankReconciliation, pk=pk)
        serializer = BankReconciliationSerializer(rec)
        return Response(serializer.data)

    def create(self, request):
        serializer = BankReconciliationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bank_reconciliation(serializer.validated_data)
            return Response({"message": "Bank reconciliation created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        rec = get_object_or_404(BankReconciliation, pk=pk)
        serializer = BankReconciliationSerializer(rec, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bank_reconciliation(rec, serializer.validated_data)
            return Response({"message": "Bank reconciliation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        rec = get_object_or_404(BankReconciliation, pk=pk)
        serializer = BankReconciliationSerializer(rec, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bank_reconciliation(rec, serializer.validated_data)
            return Response({"message": "Bank reconciliation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rec = get_object_or_404(BankReconciliation, pk=pk)
        services.delete_bank_reconciliation(rec)
        return Response({"message": "Bank reconciliation deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BUDGET VIEWSET
# ===========================================================================

class BudgetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        budgets = services.get_all_budgets()
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        budget = services.get_budget_with_lines(pk)
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    def create(self, request):
        serializer = BudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_budget(serializer.validated_data)
            return Response({"message": "Budget created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        budget = get_object_or_404(Budget, pk=pk)
        serializer = BudgetSerializer(budget, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_budget(budget, serializer.validated_data)
            return Response({"message": "Budget updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        budget = get_object_or_404(Budget, pk=pk)
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_budget(budget, serializer.validated_data)
            return Response({"message": "Budget updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        budget = get_object_or_404(Budget, pk=pk)
        services.delete_budget(budget)
        return Response({"message": "Budget deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# FIXED ASSET VIEWSET
# ===========================================================================

class FixedAssetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        assets = services.get_all_fixed_assets()
        serializer = FixedAssetSerializer(assets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        asset = get_object_or_404(FixedAsset, pk=pk)
        serializer = FixedAssetSerializer(asset)
        return Response(serializer.data)

    def create(self, request):
        serializer = FixedAssetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_fixed_asset(serializer.validated_data)
            return Response({"message": "Fixed asset created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        asset = get_object_or_404(FixedAsset, pk=pk)
        serializer = FixedAssetSerializer(asset, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_fixed_asset(asset, serializer.validated_data)
            return Response({"message": "Fixed asset updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        asset = get_object_or_404(FixedAsset, pk=pk)
        serializer = FixedAssetSerializer(asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_fixed_asset(asset, serializer.validated_data)
            return Response({"message": "Fixed asset updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        asset = get_object_or_404(FixedAsset, pk=pk)
        services.delete_fixed_asset(asset)
        return Response({"message": "Fixed asset deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# RECEIVABLE VIEWSET
# ===========================================================================

class ReceivableViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        receivables = services.get_all_receivables()
        serializer = ReceivableSerializer(receivables, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        receivable = services.get_receivable_with_payments(pk)
        serializer = ReceivableSerializer(receivable)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReceivableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_receivable(serializer.validated_data)
            return Response({"message": "Receivable created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        receivable = get_object_or_404(Receivable, pk=pk)
        serializer = ReceivableSerializer(receivable, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_receivable(receivable, serializer.validated_data)
            return Response({"message": "Receivable updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        receivable = get_object_or_404(Receivable, pk=pk)
        serializer = ReceivableSerializer(receivable, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_receivable(receivable, serializer.validated_data)
            return Response({"message": "Receivable updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        receivable = get_object_or_404(Receivable, pk=pk)
        services.delete_receivable(receivable)
        return Response({"message": "Receivable deleted successfully."}, status=status.HTTP_200_OK)
