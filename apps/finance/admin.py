from django.contrib import admin
from .models import (
    ChartOfAccount, Journal, JournalEntry, BankAccount, BankTransaction,
    BankReconciliation, Budget, BudgetLine, FixedAsset, Receivable, ReceivablePayment,
)


@admin.register(ChartOfAccount)
class ChartOfAccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type', 'parent', 'level', 'opening_balance', 'current_balance', 'is_posting', 'status', 'currency', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('type', 'status', 'is_posting', 'currency')


class JournalEntryInline(admin.TabularInline):
    model = JournalEntry
    extra = 0


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('journal_number', 'date', 'type', 'reference', 'total_debit', 'total_credit', 'status', 'posted_by', 'posted_at', 'created_at')
    search_fields = ('journal_number', 'reference')
    list_filter = ('type', 'status')
    inlines = [JournalEntryInline]


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('journal', 'account_code', 'account_name', 'cost_center', 'debit', 'credit', 'currency', 'exchange_rate')
    search_fields = ('account_code', 'account_name')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_number', 'bank_name', 'branch', 'currency', 'opening_balance', 'current_balance', 'status', 'created_at')
    search_fields = ('account_name', 'account_number', 'bank_name')
    list_filter = ('status', 'currency')


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'txn_date', 'reference', 'debit', 'credit', 'balance', 'txn_type', 'is_reconciled', 'created_at')
    search_fields = ('reference', 'description')
    list_filter = ('is_reconciled', 'txn_type')


@admin.register(BankReconciliation)
class BankReconciliationAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'statement_date', 'statement_balance', 'book_balance', 'difference', 'status', 'reconciled_by', 'reconciled_at', 'created_at')
    search_fields = ('bank_account__account_name',)
    list_filter = ('status',)


class BudgetLineInline(admin.TabularInline):
    model = BudgetLine
    extra = 0


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('budget_code', 'name', 'fiscal_year', 'start_date', 'end_date', 'total_amount', 'spent_amount', 'status', 'approved_by', 'created_at')
    search_fields = ('budget_code', 'name', 'fiscal_year')
    list_filter = ('status', 'fiscal_year')
    inlines = [BudgetLineInline]


@admin.register(BudgetLine)
class BudgetLineAdmin(admin.ModelAdmin):
    list_display = ('budget', 'account_name', 'cost_center', 'budgeted_amount', 'actual_amount', 'variance', 'month')
    search_fields = ('account_name',)


@admin.register(FixedAsset)
class FixedAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_code', 'name', 'category', 'purchase_date', 'purchase_cost', 'accumulated_dep', 'net_book_value', 'status', 'location', 'created_at')
    search_fields = ('asset_code', 'name')
    list_filter = ('status', 'category', 'depreciation_method')


class ReceivablePaymentInline(admin.TabularInline):
    model = ReceivablePayment
    extra = 0


@admin.register(Receivable)
class ReceivableAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer_name', 'invoice_date', 'due_date', 'currency', 'total_amount', 'paid_amount', 'balance', 'status', 'created_at')
    search_fields = ('invoice_number', 'customer_name')
    list_filter = ('status', 'currency')
    inlines = [ReceivablePaymentInline]


@admin.register(ReceivablePayment)
class ReceivablePaymentAdmin(admin.ModelAdmin):
    list_display = ('receivable', 'amount', 'payment_date', 'method', 'reference', 'bank_account', 'created_at')
    search_fields = ('reference',)
    list_filter = ('method',)
