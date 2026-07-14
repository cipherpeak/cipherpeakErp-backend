from django.contrib import admin
from .models import (
    SalaryStructure, SalaryComponent, PayrollRun, PayrollEntry,
    Payslip, PayslipComponent, Bonus, PayrollDeduction,
    Loan, LoanRepaymentSchedule, StatutoryFiling,
)


class SalaryComponentInline(admin.TabularInline):
    model = SalaryComponent
    extra = 0


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('structure_code', 'name', 'applicable_to', 'tax_regime', 'currency', 'status', 'basic_salary', 'net_salary', 'employee_count', 'created_at')
    search_fields = ('structure_code', 'name')
    list_filter = ('status', 'tax_regime', 'currency')
    inlines = [SalaryComponentInline]


class PayrollEntryInline(admin.TabularInline):
    model = PayrollEntry
    extra = 0


@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ('run_number', 'period_month', 'period_year', 'pay_date', 'status', 'employee_count', 'total_earnings', 'total_deductions', 'total_net', 'created_at')
    search_fields = ('run_number', 'wps_reference')
    list_filter = ('status', 'period_year')
    inlines = [PayrollEntryInline]


class PayslipComponentInline(admin.TabularInline):
    model = PayslipComponent
    extra = 0


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('payslip_number', 'employee', 'period_month', 'period_year', 'total_earnings', 'total_deductions', 'net_salary', 'payment_date', 'status', 'created_at')
    search_fields = ('payslip_number',)
    list_filter = ('status', 'period_year')
    inlines = [PayslipComponentInline]


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('bonus_number', 'employee', 'bonus_type', 'period', 'amount', 'status', 'approval_date', 'pay_date', 'created_at')
    search_fields = ('bonus_number',)
    list_filter = ('bonus_type', 'status')


@admin.register(PayrollDeduction)
class PayrollDeductionAdmin(admin.ModelAdmin):
    list_display = ('deduction_number', 'employee', 'deduction_type', 'amount', 'period_month', 'period_year', 'status', 'created_at')
    search_fields = ('deduction_number', 'deduction_type', 'reference_number')
    list_filter = ('status',)


class LoanRepaymentScheduleInline(admin.TabularInline):
    model = LoanRepaymentSchedule
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_number', 'employee', 'loan_type', 'amount_approved', 'emi_amount', 'tenure_months', 'status', 'installments_paid', 'outstanding_balance', 'created_at')
    search_fields = ('loan_number',)
    list_filter = ('loan_type', 'status')
    inlines = [LoanRepaymentScheduleInline]


@admin.register(StatutoryFiling)
class StatutoryFilingAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'type', 'country', 'period', 'due_date', 'filing_date', 'total_amount', 'status', 'created_at')
    search_fields = ('reference_number', 'period')
    list_filter = ('type', 'status', 'country')
