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


class ComponentType(models.TextChoices):
    EARNING = 'earning', 'Earning'
    DEDUCTION = 'deduction', 'Deduction'


class ComponentBasis(models.TextChoices):
    FIXED = 'fixed', 'Fixed'
    PERCENTAGE_OF_BASIC = 'percentage_of_basic', 'Percentage of Basic'
    PERCENTAGE_OF_GROSS = 'percentage_of_gross', 'Percentage of Gross'


class StructureStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    DRAFT = 'draft', 'Draft'


class TaxRegime(models.TextChoices):
    UAE = 'UAE', 'UAE'
    INDIA = 'India', 'India'


class PayrollRunStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    IN_PROGRESS = 'in_progress', 'In Progress'
    PROCESSING = 'processing', 'Processing'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    SUBMITTED = 'submitted', 'Submitted'
    APPROVED = 'approved', 'Approved'
    PROCESSED = 'processed', 'Processed'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'


class PayslipStatus(models.TextChoices):
    GENERATED = 'generated', 'Generated'
    PUBLISHED = 'published', 'Published'
    SENT = 'sent', 'Sent'
    VIEWED = 'viewed', 'Viewed'
    ACKNOWLEDGED = 'acknowledged', 'Acknowledged'


class BonusType(models.TextChoices):
    PERFORMANCE = 'performance', 'Performance'
    ANNUAL = 'annual', 'Annual'
    FESTIVE = 'festive', 'Festive'
    RETENTION = 'retention', 'Retention'
    PROJECT = 'project', 'Project'
    REFERRAL = 'referral', 'Referral'


class BonusStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    PAID = 'paid', 'Paid'
    REJECTED = 'rejected', 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'


class LoanType(models.TextChoices):
    PERSONAL_LOAN = 'personal_loan', 'Personal Loan'
    HOUSING_LOAN = 'housing_loan', 'Housing Loan'
    VEHICLE_LOAN = 'vehicle_loan', 'Vehicle Loan'
    EMERGENCY_ADVANCE = 'emergency_advance', 'Emergency Advance'
    SALARY_ADVANCE = 'salary_advance', 'Salary Advance'


class LoanStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    DISBURSED = 'disbursed', 'Disbursed'
    ACTIVE = 'active', 'Active'
    FULLY_REPAID = 'fully_repaid', 'Fully Repaid'
    CLOSED = 'closed', 'Closed'
    REJECTED = 'rejected', 'Rejected'


class DeductionStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DEDUCTED = 'deducted', 'Deducted'
    WAIVED = 'waived', 'Waived'
    CANCELLED = 'cancelled', 'Cancelled'
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    APPLIED = 'applied', 'Applied'
    REJECTED = 'rejected', 'Rejected'


class StatutoryType(models.TextChoices):
    WPS = 'WPS', 'WPS'
    GPSSA = 'GPSSA', 'GPSSA'
    DEWS = 'DEWS', 'DEWS'
    DIFC_DEWS = 'DIFC_DEWS', 'DIFC DEWS'
    PF = 'PF', 'PF'
    ESI = 'ESI', 'ESI'
    TDS = 'TDS', 'TDS'
    PROFESSIONAL_TAX = 'professional_tax', 'Professional Tax'


class StatutoryStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    FILED = 'filed', 'Filed'
    PAID = 'paid', 'Paid'
    OVERDUE = 'overdue', 'Overdue'
    EXEMPTED = 'exempted', 'Exempted'


# ---------------------------------------------------------------------------
# Salary Structure
# ---------------------------------------------------------------------------

class SalaryStructure(models.Model):
    structure_code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    applicable_to = models.CharField(max_length=150, blank=True, null=True)
    tax_regime = models.CharField(max_length=20, choices=TaxRegime.choices, default=TaxRegime.UAE)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    status = models.CharField(max_length=20, choices=StructureStatus.choices, default=StructureStatus.DRAFT)
    effective_from = models.DateField(blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_gross = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    employee_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_salary_structures',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Salary Structure'
        verbose_name_plural = 'Salary Structures'
        ordering = ['structure_code']

    def __str__(self):
        return f"{self.structure_code} - {self.name}"


class SalaryComponent(models.Model):
    structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=20, choices=ComponentType.choices)
    basis = models.CharField(max_length=30, choices=ComponentBasis.choices, default=ComponentBasis.FIXED)
    value = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    taxable = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Salary Component'
        verbose_name_plural = 'Salary Components'

    def __str__(self):
        return f"{self.structure.structure_code} - {self.name}"


# ---------------------------------------------------------------------------
# Payroll Run
# ---------------------------------------------------------------------------

class PayrollRun(models.Model):
    run_number = models.CharField(max_length=40, unique=True)
    period_month = models.CharField(max_length=20)
    period_year = models.SmallIntegerField()
    pay_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PayrollRunStatus.choices, default=PayrollRunStatus.DRAFT)
    employee_count = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_net = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    prepared_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='prepared_payroll_runs',
    )
    approved_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_payroll_runs',
    )
    wps_reference = models.CharField(max_length=60, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payroll Run'
        verbose_name_plural = 'Payroll Runs'
        ordering = ['-created_at']

    def __str__(self):
        return self.run_number


class PayrollEntry(models.Model):
    run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='entries')
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='payroll_entries')
    salary_structure = models.ForeignKey(
        SalaryStructure, on_delete=models.SET_NULL, blank=True, null=True, related_name='payroll_entries',
    )
    working_days = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    actual_days = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    absent_days = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    leave_days_paid = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    leave_days_unpaid = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_earnings = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bank_account = models.CharField(max_length=60, blank=True, null=True)
    earnings = models.JSONField(default=dict, blank=True)
    deductions = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Payroll Entry'
        verbose_name_plural = 'Payroll Entries'

    def __str__(self):
        return f"{self.run.run_number} - {self.employee}"


# ---------------------------------------------------------------------------
# Payslip
# ---------------------------------------------------------------------------

class Payslip(models.Model):
    payslip_number = models.CharField(max_length=40, unique=True)
    run = models.ForeignKey(
        PayrollRun, on_delete=models.SET_NULL, blank=True, null=True, related_name='payslips',
    )
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='payslips')
    period_month = models.CharField(max_length=20)
    period_year = models.SmallIntegerField()
    salary_structure = models.ForeignKey(
        SalaryStructure, on_delete=models.SET_NULL, blank=True, null=True, related_name='payslips',
    )
    bank_name = models.CharField(max_length=120, blank=True, null=True)
    bank_account = models.CharField(max_length=60, blank=True, null=True)
    iban = models.CharField(max_length=40, blank=True, null=True)
    working_days = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    actual_working_days = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    absent_days = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    leave_days_paid = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    leave_days_unpaid = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    total_earnings = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    ytd_gross = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    ytd_deductions = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    ytd_net = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PayslipStatus.choices, default=PayslipStatus.GENERATED)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payslip'
        verbose_name_plural = 'Payslips'
        ordering = ['-created_at']

    def __str__(self):
        return self.payslip_number


class PayslipComponent(models.Model):
    payslip = models.ForeignKey(Payslip, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=ComponentType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        verbose_name = 'Payslip Component'
        verbose_name_plural = 'Payslip Components'

    def __str__(self):
        return f"{self.payslip.payslip_number} - {self.name}"


# ---------------------------------------------------------------------------
# Bonus
# ---------------------------------------------------------------------------

class Bonus(models.Model):
    bonus_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='bonuses')
    bonus_type = models.CharField(max_length=20, choices=BonusType.choices)
    period = models.CharField(max_length=40, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    tax_applicable = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=BonusStatus.choices, default=BonusStatus.DRAFT)
    recommended_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='recommended_bonuses',
    )
    approved_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_bonuses',
    )
    approval_date = models.DateField(blank=True, null=True)
    pay_date = models.DateField(blank=True, null=True)
    pay_with_salary = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonuses'
        ordering = ['-created_at']

    def __str__(self):
        return self.bonus_number


# ---------------------------------------------------------------------------
# Payroll Deduction
# ---------------------------------------------------------------------------

class PayrollDeduction(models.Model):
    deduction_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='payroll_deductions')
    deduction_type = models.CharField(max_length=60)
    reason = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    period_month = models.CharField(max_length=20, blank=True, null=True)
    period_year = models.SmallIntegerField(blank=True, null=True)
    salary_run = models.ForeignKey(
        PayrollRun, on_delete=models.SET_NULL, blank=True, null=True, related_name='deductions',
    )
    status = models.CharField(max_length=20, choices=DeductionStatus.choices, default=DeductionStatus.PENDING)
    approved_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_deductions',
    )
    reference_number = models.CharField(max_length=60, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payroll Deduction'
        verbose_name_plural = 'Payroll Deductions'
        ordering = ['-created_at']

    def __str__(self):
        return self.deduction_number


# ---------------------------------------------------------------------------
# Loan
# ---------------------------------------------------------------------------

class Loan(models.Model):
    loan_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=30, choices=LoanType.choices)
    purpose = models.TextField(blank=True, null=True)
    amount_requested = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    amount_approved = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tenure_months = models.IntegerField(blank=True, null=True)
    emi_amount = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    applied_date = models.DateField(blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    disbursement_date = models.DateField(blank=True, null=True)
    first_emi_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=LoanStatus.choices, default=LoanStatus.DRAFT)
    approved_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_loans',
    )
    installments_paid = models.IntegerField(default=0)
    total_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    deduction_from_salary = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
        ordering = ['-created_at']

    def __str__(self):
        return self.loan_number


class LoanRepaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayment_schedule')
    installment_number = models.IntegerField()
    due_date = models.DateField(blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    emi_amount = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    principal = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    interest = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    closing_balance = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', help_text='paid/pending/overdue')
    paid_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Loan Repayment Schedule'
        verbose_name_plural = 'Loan Repayment Schedules'
        ordering = ['installment_number']

    def __str__(self):
        return f"{self.loan.loan_number} - #{self.installment_number}"


# ---------------------------------------------------------------------------
# Statutory Filing
# ---------------------------------------------------------------------------

class StatutoryFiling(models.Model):
    reference_number = models.CharField(max_length=60, unique=True)
    type = models.CharField(max_length=30, choices=StatutoryType.choices)
    country = models.CharField(max_length=20, help_text='UAE/India')
    period = models.CharField(max_length=40, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    filing_date = models.DateField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    employer_contribution = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    employee_contribution = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=StatutoryStatus.choices, default=StatutoryStatus.PENDING)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Statutory Filing'
        verbose_name_plural = 'Statutory Filings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_number} - {self.type}"
