from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CurrencyCode(models.TextChoices):
    AED = 'AED', 'AED'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    INR = 'INR', 'INR'
    SAR = 'SAR', 'SAR'


class ActiveInactive(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class AccountType(models.TextChoices):
    ASSETS = 'Assets', 'Assets'
    LIABILITIES = 'Liabilities', 'Liabilities'
    EQUITY = 'Equity', 'Equity'
    REVENUE = 'Revenue', 'Revenue'
    EXPENSES = 'Expenses', 'Expenses'


class AccountStatus(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'


class JournalStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    POSTED = 'posted', 'Posted'
    CANCELLED = 'cancelled', 'Cancelled'


class JournalType(models.TextChoices):
    GENERAL = 'general', 'General'
    PURCHASE = 'purchase', 'Purchase'
    SALE = 'sale', 'Sale'
    PAYMENT = 'payment', 'Payment'
    RECEIPT = 'receipt', 'Receipt'
    ADJUSTING = 'adjusting', 'Adjusting'
    OPENING = 'opening', 'Opening'
    CLOSING = 'closing', 'Closing'


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Cash'
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    CHEQUE = 'cheque', 'Cheque'
    ONLINE = 'online', 'Online'


# ---------------------------------------------------------------------------
# Chart of Accounts
# ---------------------------------------------------------------------------

class ChartOfAccount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=300)
    type = models.CharField(max_length=20, choices=AccountType.choices)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children',
    )
    level = models.SmallIntegerField(default=0)
    opening_balance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    current_balance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    is_posting = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    description = models.TextField(blank=True, null=True)
    cost_center = models.ForeignKey(
        'organization.CostCenter', on_delete=models.SET_NULL, blank=True, null=True, related_name='accounts',
    )
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chart of Account'
        verbose_name_plural = 'Chart of Accounts'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------------------------------------------------------------------
# Journals
# ---------------------------------------------------------------------------

class Journal(models.Model):
    journal_number = models.CharField(max_length=30, unique=True)
    date = models.DateField(blank=True, null=True)
    type = models.CharField(
        max_length=20,
        choices=JournalType.choices,
        default=JournalType.GENERAL,
    )
    reference = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    total_debit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    total_credit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    status = models.CharField(
        max_length=20,
        choices=JournalStatus.choices,
        default=JournalStatus.DRAFT,
    )
    posted_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='posted_journals',
    )
    posted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_journals',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Journal'
        verbose_name_plural = 'Journals'
        ordering = ['-created_at']

    def __str__(self):
        return self.journal_number


class JournalEntry(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(
        ChartOfAccount, on_delete=models.PROTECT, related_name='journal_entries',
    )
    account_code = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=300, blank=True, null=True)
    cost_center = models.ForeignKey(
        'organization.CostCenter', on_delete=models.SET_NULL, blank=True, null=True, related_name='journal_entries',
    )
    debit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    credit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1)

    class Meta:
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'

    def __str__(self):
        return f"{self.journal.journal_number} - {self.account_name}"

    def save(self, *args, **kwargs):
        if self.account and not self.account_name:
            self.account_name = self.account.name
            self.account_code = self.account.code
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Bank Accounts
# ---------------------------------------------------------------------------

class BankAccount(models.Model):
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=200, blank=True, null=True)
    ifsc = models.CharField(max_length=20, blank=True, null=True)
    swift = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    gl_account = models.ForeignKey(
        ChartOfAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='bank_accounts',
    )
    opening_balance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    current_balance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    status = models.CharField(
        max_length=20,
        choices=ActiveInactive.choices,
        default=ActiveInactive.ACTIVE,
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'
        ordering = ['account_name']

    def __str__(self):
        return f"{self.account_name} ({self.account_number})"


class BankReconciliation(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='reconciliations')
    statement_date = models.DateField()
    statement_balance = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    book_balance = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    difference = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    status = models.CharField(max_length=30, default='open', help_text='open/reconciled')
    reconciled_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='reconciliations',
    )
    reconciled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bank Reconciliation'
        verbose_name_plural = 'Bank Reconciliations'
        ordering = ['-statement_date']

    def __str__(self):
        return f"{self.bank_account.account_name} - {self.statement_date}"


class BankTransaction(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    txn_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    debit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    credit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    balance = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    txn_type = models.CharField(max_length=50, blank=True, null=True)
    is_reconciled = models.BooleanField(default=False)
    reconciliation = models.ForeignKey(
        BankReconciliation, on_delete=models.SET_NULL, blank=True, null=True, related_name='transactions',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bank Transaction'
        verbose_name_plural = 'Bank Transactions'
        ordering = ['-txn_date']

    def __str__(self):
        return f"{self.bank_account.account_name} - {self.txn_date}"


# ---------------------------------------------------------------------------
# Budgets
# ---------------------------------------------------------------------------

class Budget(models.Model):
    budget_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    fiscal_year = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    spent_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    status = models.CharField(max_length=30, default='draft', help_text='draft/approved/active/closed')
    notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_budgets',
    )
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_budgets',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.budget_code} - {self.name}"


class BudgetLine(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(
        ChartOfAccount, on_delete=models.PROTECT, related_name='budget_lines',
    )
    account_name = models.CharField(max_length=300, blank=True, null=True)
    cost_center = models.ForeignKey(
        'organization.CostCenter', on_delete=models.SET_NULL, blank=True, null=True, related_name='budget_lines',
    )
    budgeted_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    actual_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    variance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    month = models.SmallIntegerField(blank=True, null=True, help_text='1-12')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Budget Line'
        verbose_name_plural = 'Budget Lines'

    def __str__(self):
        return f"{self.budget.budget_code} - {self.account_name}"

    def save(self, *args, **kwargs):
        if self.account and not self.account_name:
            self.account_name = self.account.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Fixed Assets
# ---------------------------------------------------------------------------

class FixedAsset(models.Model):
    asset_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=100, blank=True, null=True)
    gl_account = models.ForeignKey(
        ChartOfAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='fixed_assets',
    )
    cost_center = models.ForeignKey(
        'organization.CostCenter', on_delete=models.SET_NULL, blank=True, null=True, related_name='fixed_assets',
    )
    purchase_date = models.DateField(blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    useful_life_years = models.SmallIntegerField(blank=True, null=True)
    residual_value = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    depreciation_method = models.CharField(max_length=50, default='straight_line')
    accumulated_dep = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    net_book_value = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    status = models.CharField(max_length=30, default='active', help_text='active/disposed/written_off')
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fixed Asset'
        verbose_name_plural = 'Fixed Assets'
        ordering = ['asset_code']

    def __str__(self):
        return f"{self.asset_code} - {self.name}"


# ---------------------------------------------------------------------------
# Receivables
# ---------------------------------------------------------------------------

class Receivable(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=300, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True, help_text='FK to future customers table')
    invoice_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=30, default='pending', help_text='pending/partial/paid/overdue/cancelled')
    notes = models.TextField(blank=True, null=True)
    gl_account = models.ForeignKey(
        ChartOfAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='receivables',
    )
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_receivables',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Receivable'
        verbose_name_plural = 'Receivables'
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number


class ReceivablePayment(models.Model):
    receivable = models.ForeignKey(Receivable, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK_TRANSFER,
    )
    reference = models.CharField(max_length=100, blank=True, null=True)
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='receivable_payments',
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Receivable Payment'
        verbose_name_plural = 'Receivable Payments'
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.receivable.invoice_number} - {self.amount}"
