from typing import Dict, Any, List
from .models import (
    ChartOfAccount, Journal, JournalEntry, BankAccount, BankTransaction,
    BankReconciliation, Budget, BudgetLine, FixedAsset, Receivable, ReceivablePayment,
)


# ===========================================================================
# CHART OF ACCOUNTS SERVICES
# ===========================================================================

def get_all_accounts() -> List[ChartOfAccount]:
    return ChartOfAccount.objects.filter(is_deleted=False)

def create_account(data: Dict[str, Any]) -> ChartOfAccount:
    code = data.get('code')
    if ChartOfAccount.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Account with code '{code}' already exists.")
    return ChartOfAccount.objects.create(**data)

def update_account(account: ChartOfAccount, data: Dict[str, Any]) -> ChartOfAccount:
    code = data.get('code')
    if code and ChartOfAccount.objects.filter(code__iexact=code).exclude(id=account.id).exists():
        raise ValueError(f"Account with code '{code}' already exists.")
    for field, value in data.items():
        setattr(account, field, value)
    account.save()
    return account

def delete_account(account: ChartOfAccount) -> None:
    account.is_deleted = True
    account.save()


# ===========================================================================
# JOURNAL SERVICES
# ===========================================================================

def get_all_journals() -> List[Journal]:
    return Journal.objects.filter(is_deleted=False)

def get_journal_with_entries(journal_id: int) -> Journal:
    return Journal.objects.prefetch_related('entries').get(pk=journal_id)

def create_journal(data: Dict[str, Any]) -> Journal:
    journal_number = data.get('journal_number')
    if Journal.objects.filter(journal_number__iexact=journal_number).exists():
        raise ValueError(f"Journal number '{journal_number}' already exists.")
    entries_data = data.pop('entries', [])
    journal = Journal.objects.create(**data)
    for entry_data in entries_data:
        JournalEntry.objects.create(journal=journal, **entry_data)
    return journal

def update_journal(journal: Journal, data: Dict[str, Any]) -> Journal:
    journal_number = data.get('journal_number')
    if journal_number and Journal.objects.filter(
        journal_number__iexact=journal_number,
    ).exclude(id=journal.id).exists():
        raise ValueError(f"Journal number '{journal_number}' already exists.")
    data.pop('entries', None)
    for field, value in data.items():
        setattr(journal, field, value)
    journal.save()
    return journal

def delete_journal(journal: Journal) -> None:
    journal.is_deleted = True
    journal.save()


# ===========================================================================
# BANK ACCOUNT SERVICES
# ===========================================================================

def get_all_bank_accounts() -> List[BankAccount]:
    return BankAccount.objects.filter(is_deleted=False)

def create_bank_account(data: Dict[str, Any]) -> BankAccount:
    account_number = data.get('account_number')
    if BankAccount.objects.filter(account_number__iexact=account_number).exists():
        raise ValueError(f"Bank account number '{account_number}' already exists.")
    return BankAccount.objects.create(**data)

def update_bank_account(account: BankAccount, data: Dict[str, Any]) -> BankAccount:
    account_number = data.get('account_number')
    if account_number and BankAccount.objects.filter(
        account_number__iexact=account_number,
    ).exclude(id=account.id).exists():
        raise ValueError(f"Bank account number '{account_number}' already exists.")
    for field, value in data.items():
        setattr(account, field, value)
    account.save()
    return account

def delete_bank_account(account: BankAccount) -> None:
    account.is_deleted = True
    account.save()


# ===========================================================================
# BANK TRANSACTION SERVICES
# ===========================================================================

def get_all_bank_transactions() -> List[BankTransaction]:
    return BankTransaction.objects.all()

def create_bank_transaction(data: Dict[str, Any]) -> BankTransaction:
    return BankTransaction.objects.create(**data)

def update_bank_transaction(txn: BankTransaction, data: Dict[str, Any]) -> BankTransaction:
    for field, value in data.items():
        setattr(txn, field, value)
    txn.save()
    return txn

def delete_bank_transaction(txn: BankTransaction) -> None:
    txn.delete()


# ===========================================================================
# BANK RECONCILIATION SERVICES
# ===========================================================================

def get_all_bank_reconciliations() -> List[BankReconciliation]:
    return BankReconciliation.objects.all()

def create_bank_reconciliation(data: Dict[str, Any]) -> BankReconciliation:
    return BankReconciliation.objects.create(**data)

def update_bank_reconciliation(rec: BankReconciliation, data: Dict[str, Any]) -> BankReconciliation:
    for field, value in data.items():
        setattr(rec, field, value)
    rec.save()
    return rec

def delete_bank_reconciliation(rec: BankReconciliation) -> None:
    rec.delete()


# ===========================================================================
# BUDGET SERVICES
# ===========================================================================

def get_all_budgets() -> List[Budget]:
    return Budget.objects.filter(is_deleted=False)

def get_budget_with_lines(budget_id: int) -> Budget:
    return Budget.objects.prefetch_related('lines').get(pk=budget_id)

def create_budget(data: Dict[str, Any]) -> Budget:
    budget_code = data.get('budget_code')
    if Budget.objects.filter(budget_code__iexact=budget_code).exists():
        raise ValueError(f"Budget code '{budget_code}' already exists.")
    lines_data = data.pop('lines', [])
    budget = Budget.objects.create(**data)
    for line_data in lines_data:
        BudgetLine.objects.create(budget=budget, **line_data)
    return budget

def update_budget(budget: Budget, data: Dict[str, Any]) -> Budget:
    budget_code = data.get('budget_code')
    if budget_code and Budget.objects.filter(budget_code__iexact=budget_code).exclude(id=budget.id).exists():
        raise ValueError(f"Budget code '{budget_code}' already exists.")
    data.pop('lines', None)
    for field, value in data.items():
        setattr(budget, field, value)
    budget.save()
    return budget

def delete_budget(budget: Budget) -> None:
    budget.is_deleted = True
    budget.save()


# ===========================================================================
# FIXED ASSET SERVICES
# ===========================================================================

def get_all_fixed_assets() -> List[FixedAsset]:
    return FixedAsset.objects.filter(is_deleted=False)

def create_fixed_asset(data: Dict[str, Any]) -> FixedAsset:
    asset_code = data.get('asset_code')
    if FixedAsset.objects.filter(asset_code__iexact=asset_code).exists():
        raise ValueError(f"Asset code '{asset_code}' already exists.")
    return FixedAsset.objects.create(**data)

def update_fixed_asset(asset: FixedAsset, data: Dict[str, Any]) -> FixedAsset:
    asset_code = data.get('asset_code')
    if asset_code and FixedAsset.objects.filter(asset_code__iexact=asset_code).exclude(id=asset.id).exists():
        raise ValueError(f"Asset code '{asset_code}' already exists.")
    for field, value in data.items():
        setattr(asset, field, value)
    asset.save()
    return asset

def delete_fixed_asset(asset: FixedAsset) -> None:
    asset.is_deleted = True
    asset.save()


# ===========================================================================
# RECEIVABLE SERVICES
# ===========================================================================

def get_all_receivables() -> List[Receivable]:
    return Receivable.objects.filter(is_deleted=False)

def get_receivable_with_payments(receivable_id: int) -> Receivable:
    return Receivable.objects.prefetch_related('payments').get(pk=receivable_id)

def create_receivable(data: Dict[str, Any]) -> Receivable:
    invoice_number = data.get('invoice_number')
    if Receivable.objects.filter(invoice_number__iexact=invoice_number).exists():
        raise ValueError(f"Invoice number '{invoice_number}' already exists.")
    payments_data = data.pop('payments', [])
    receivable = Receivable.objects.create(**data)
    for payment_data in payments_data:
        ReceivablePayment.objects.create(receivable=receivable, **payment_data)
    return receivable

def update_receivable(receivable: Receivable, data: Dict[str, Any]) -> Receivable:
    invoice_number = data.get('invoice_number')
    if invoice_number and Receivable.objects.filter(
        invoice_number__iexact=invoice_number,
    ).exclude(id=receivable.id).exists():
        raise ValueError(f"Invoice number '{invoice_number}' already exists.")
    data.pop('payments', None)
    for field, value in data.items():
        setattr(receivable, field, value)
    receivable.save()
    return receivable

def delete_receivable(receivable: Receivable) -> None:
    receivable.is_deleted = True
    receivable.save()
