from rest_framework import serializers
from .models import (
    SalaryStructure, SalaryComponent, PayrollRun, PayrollEntry,
    Payslip, PayslipComponent, Bonus, PayrollDeduction,
    Loan, LoanRepaymentSchedule, StatutoryFiling,
)


# ===========================================================================
# SALARY STRUCTURE SERIALIZERS
# ===========================================================================

class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = '__all__'
        extra_kwargs = {'structure': {'required': False}}


class SalaryStructureSerializer(serializers.ModelSerializer):
    components = SalaryComponentSerializer(many=True, required=False)

    class Meta:
        model = SalaryStructure
        fields = '__all__'


# ===========================================================================
# PAYROLL RUN SERIALIZERS
# ===========================================================================

class PayrollEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollEntry
        fields = '__all__'
        extra_kwargs = {'run': {'required': False}}


class PayrollRunSerializer(serializers.ModelSerializer):
    entries = PayrollEntrySerializer(many=True, required=False)

    class Meta:
        model = PayrollRun
        fields = '__all__'


# ===========================================================================
# PAYSLIP SERIALIZERS
# ===========================================================================

class PayslipComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayslipComponent
        fields = '__all__'
        extra_kwargs = {'payslip': {'required': False}}


class PayslipSerializer(serializers.ModelSerializer):
    components = PayslipComponentSerializer(many=True, required=False)

    class Meta:
        model = Payslip
        fields = '__all__'


# ===========================================================================
# BONUS SERIALIZER
# ===========================================================================

class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'


# ===========================================================================
# PAYROLL DEDUCTION SERIALIZER
# ===========================================================================

class PayrollDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeduction
        fields = '__all__'


# ===========================================================================
# LOAN SERIALIZERS
# ===========================================================================

class LoanRepaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepaymentSchedule
        fields = '__all__'
        extra_kwargs = {'loan': {'required': False}}


class LoanSerializer(serializers.ModelSerializer):
    repayment_schedule = LoanRepaymentScheduleSerializer(many=True, required=False)

    class Meta:
        model = Loan
        fields = '__all__'


# ===========================================================================
# STATUTORY FILING SERIALIZER
# ===========================================================================

class StatutoryFilingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutoryFiling
        fields = '__all__'
