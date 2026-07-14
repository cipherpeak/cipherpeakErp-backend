from typing import Dict, Any, List
from .models import (
    SalaryStructure, SalaryComponent, PayrollRun, PayrollEntry,
    Payslip, PayslipComponent, Bonus, PayrollDeduction,
    Loan, LoanRepaymentSchedule, StatutoryFiling,
)


# ===========================================================================
# SALARY STRUCTURE SERVICES
# ===========================================================================

def get_all_salary_structures() -> List[SalaryStructure]:
    return SalaryStructure.objects.filter(is_deleted=False)

def get_salary_structure_with_components(structure_id: int) -> SalaryStructure:
    return SalaryStructure.objects.prefetch_related('components').get(pk=structure_id)

def create_salary_structure(data: Dict[str, Any]) -> SalaryStructure:
    structure_code = data.get('structure_code')
    if SalaryStructure.objects.filter(structure_code__iexact=structure_code).exists():
        raise ValueError(f"Structure code '{structure_code}' already exists.")
    components_data = data.pop('components', [])
    structure = SalaryStructure.objects.create(**data)
    for comp_data in components_data:
        SalaryComponent.objects.create(structure=structure, **comp_data)
    return structure

def update_salary_structure(structure: SalaryStructure, data: Dict[str, Any]) -> SalaryStructure:
    structure_code = data.get('structure_code')
    if structure_code and SalaryStructure.objects.filter(
        structure_code__iexact=structure_code,
    ).exclude(id=structure.id).exists():
        raise ValueError(f"Structure code '{structure_code}' already exists.")
    data.pop('components', None)
    for field, value in data.items():
        setattr(structure, field, value)
    structure.save()
    return structure

def delete_salary_structure(structure: SalaryStructure) -> None:
    structure.is_deleted = True
    structure.save()


# ===========================================================================
# PAYROLL RUN SERVICES
# ===========================================================================

def get_all_payroll_runs() -> List[PayrollRun]:
    return PayrollRun.objects.filter(is_deleted=False)

def get_payroll_run_with_entries(run_id: int) -> PayrollRun:
    return PayrollRun.objects.prefetch_related('entries').get(pk=run_id)

def create_payroll_run(data: Dict[str, Any]) -> PayrollRun:
    run_number = data.get('run_number')
    if PayrollRun.objects.filter(run_number__iexact=run_number).exists():
        raise ValueError(f"Run number '{run_number}' already exists.")
    entries_data = data.pop('entries', [])
    run = PayrollRun.objects.create(**data)
    for entry_data in entries_data:
        PayrollEntry.objects.create(run=run, **entry_data)
    return run

def update_payroll_run(run: PayrollRun, data: Dict[str, Any]) -> PayrollRun:
    run_number = data.get('run_number')
    if run_number and PayrollRun.objects.filter(run_number__iexact=run_number).exclude(id=run.id).exists():
        raise ValueError(f"Run number '{run_number}' already exists.")
    data.pop('entries', None)
    for field, value in data.items():
        setattr(run, field, value)
    run.save()
    return run

def delete_payroll_run(run: PayrollRun) -> None:
    run.is_deleted = True
    run.save()


# ===========================================================================
# PAYSLIP SERVICES
# ===========================================================================

def get_all_payslips() -> List[Payslip]:
    return Payslip.objects.filter(is_deleted=False)

def get_payslip_with_components(payslip_id: int) -> Payslip:
    return Payslip.objects.prefetch_related('components').get(pk=payslip_id)

def create_payslip(data: Dict[str, Any]) -> Payslip:
    payslip_number = data.get('payslip_number')
    if Payslip.objects.filter(payslip_number__iexact=payslip_number).exists():
        raise ValueError(f"Payslip number '{payslip_number}' already exists.")
    components_data = data.pop('components', [])
    payslip = Payslip.objects.create(**data)
    for comp_data in components_data:
        PayslipComponent.objects.create(payslip=payslip, **comp_data)
    return payslip

def update_payslip(payslip: Payslip, data: Dict[str, Any]) -> Payslip:
    payslip_number = data.get('payslip_number')
    if payslip_number and Payslip.objects.filter(
        payslip_number__iexact=payslip_number,
    ).exclude(id=payslip.id).exists():
        raise ValueError(f"Payslip number '{payslip_number}' already exists.")
    data.pop('components', None)
    for field, value in data.items():
        setattr(payslip, field, value)
    payslip.save()
    return payslip

def delete_payslip(payslip: Payslip) -> None:
    payslip.is_deleted = True
    payslip.save()


# ===========================================================================
# BONUS SERVICES
# ===========================================================================

def get_all_bonuses() -> List[Bonus]:
    return Bonus.objects.filter(is_deleted=False)

def create_bonus(data: Dict[str, Any]) -> Bonus:
    bonus_number = data.get('bonus_number')
    if Bonus.objects.filter(bonus_number__iexact=bonus_number).exists():
        raise ValueError(f"Bonus number '{bonus_number}' already exists.")
    return Bonus.objects.create(**data)

def update_bonus(bonus: Bonus, data: Dict[str, Any]) -> Bonus:
    bonus_number = data.get('bonus_number')
    if bonus_number and Bonus.objects.filter(bonus_number__iexact=bonus_number).exclude(id=bonus.id).exists():
        raise ValueError(f"Bonus number '{bonus_number}' already exists.")
    for field, value in data.items():
        setattr(bonus, field, value)
    bonus.save()
    return bonus

def delete_bonus(bonus: Bonus) -> None:
    bonus.is_deleted = True
    bonus.save()


# ===========================================================================
# PAYROLL DEDUCTION SERVICES
# ===========================================================================

def get_all_deductions() -> List[PayrollDeduction]:
    return PayrollDeduction.objects.filter(is_deleted=False)

def create_deduction(data: Dict[str, Any]) -> PayrollDeduction:
    deduction_number = data.get('deduction_number')
    if PayrollDeduction.objects.filter(deduction_number__iexact=deduction_number).exists():
        raise ValueError(f"Deduction number '{deduction_number}' already exists.")
    return PayrollDeduction.objects.create(**data)

def update_deduction(deduction: PayrollDeduction, data: Dict[str, Any]) -> PayrollDeduction:
    deduction_number = data.get('deduction_number')
    if deduction_number and PayrollDeduction.objects.filter(
        deduction_number__iexact=deduction_number,
    ).exclude(id=deduction.id).exists():
        raise ValueError(f"Deduction number '{deduction_number}' already exists.")
    for field, value in data.items():
        setattr(deduction, field, value)
    deduction.save()
    return deduction

def delete_deduction(deduction: PayrollDeduction) -> None:
    deduction.is_deleted = True
    deduction.save()


# ===========================================================================
# LOAN SERVICES
# ===========================================================================

def get_all_loans() -> List[Loan]:
    return Loan.objects.filter(is_deleted=False)

def get_loan_with_schedule(loan_id: int) -> Loan:
    return Loan.objects.prefetch_related('repayment_schedule').get(pk=loan_id)

def create_loan(data: Dict[str, Any]) -> Loan:
    loan_number = data.get('loan_number')
    if Loan.objects.filter(loan_number__iexact=loan_number).exists():
        raise ValueError(f"Loan number '{loan_number}' already exists.")
    schedule_data = data.pop('repayment_schedule', [])
    loan = Loan.objects.create(**data)
    for sched_data in schedule_data:
        LoanRepaymentSchedule.objects.create(loan=loan, **sched_data)
    return loan

def update_loan(loan: Loan, data: Dict[str, Any]) -> Loan:
    loan_number = data.get('loan_number')
    if loan_number and Loan.objects.filter(loan_number__iexact=loan_number).exclude(id=loan.id).exists():
        raise ValueError(f"Loan number '{loan_number}' already exists.")
    data.pop('repayment_schedule', None)
    for field, value in data.items():
        setattr(loan, field, value)
    loan.save()
    return loan

def delete_loan(loan: Loan) -> None:
    loan.is_deleted = True
    loan.save()


# ===========================================================================
# STATUTORY FILING SERVICES
# ===========================================================================

def get_all_statutory_filings() -> List[StatutoryFiling]:
    return StatutoryFiling.objects.filter(is_deleted=False)

def create_statutory_filing(data: Dict[str, Any]) -> StatutoryFiling:
    reference_number = data.get('reference_number')
    if StatutoryFiling.objects.filter(reference_number__iexact=reference_number).exists():
        raise ValueError(f"Reference number '{reference_number}' already exists.")
    return StatutoryFiling.objects.create(**data)

def update_statutory_filing(filing: StatutoryFiling, data: Dict[str, Any]) -> StatutoryFiling:
    reference_number = data.get('reference_number')
    if reference_number and StatutoryFiling.objects.filter(
        reference_number__iexact=reference_number,
    ).exclude(id=filing.id).exists():
        raise ValueError(f"Reference number '{reference_number}' already exists.")
    for field, value in data.items():
        setattr(filing, field, value)
    filing.save()
    return filing

def delete_statutory_filing(filing: StatutoryFiling) -> None:
    filing.is_deleted = True
    filing.save()
