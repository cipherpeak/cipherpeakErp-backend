from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    SalaryStructure, PayrollRun, Payslip, Bonus, PayrollDeduction, Loan, StatutoryFiling,
)
from .serializers import (
    SalaryStructureSerializer, PayrollRunSerializer, PayslipSerializer, BonusSerializer,
    PayrollDeductionSerializer, LoanSerializer, StatutoryFilingSerializer,
)
from . import services


# ===========================================================================
# SALARY STRUCTURE VIEWSET
# ===========================================================================

class SalaryStructureViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        structures = services.get_all_salary_structures()
        return Response(SalaryStructureSerializer(structures, many=True).data)

    def retrieve(self, request, pk=None):
        structure = services.get_salary_structure_with_components(pk)
        return Response(SalaryStructureSerializer(structure).data)

    def create(self, request):
        serializer = SalaryStructureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_salary_structure(serializer.validated_data)
            return Response({"message": "Salary structure created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        structure = get_object_or_404(SalaryStructure, pk=pk)
        serializer = SalaryStructureSerializer(structure, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_salary_structure(structure, serializer.validated_data)
            return Response({"message": "Salary structure updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        structure = get_object_or_404(SalaryStructure, pk=pk)
        serializer = SalaryStructureSerializer(structure, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_salary_structure(structure, serializer.validated_data)
            return Response({"message": "Salary structure updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        structure = get_object_or_404(SalaryStructure, pk=pk)
        services.delete_salary_structure(structure)
        return Response({"message": "Salary structure deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PAYROLL RUN VIEWSET
# ===========================================================================

class PayrollRunViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        runs = services.get_all_payroll_runs()
        return Response(PayrollRunSerializer(runs, many=True).data)

    def retrieve(self, request, pk=None):
        run = services.get_payroll_run_with_entries(pk)
        return Response(PayrollRunSerializer(run).data)

    def create(self, request):
        serializer = PayrollRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_payroll_run(serializer.validated_data)
            return Response({"message": "Payroll run created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        run = get_object_or_404(PayrollRun, pk=pk)
        serializer = PayrollRunSerializer(run, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_payroll_run(run, serializer.validated_data)
            return Response({"message": "Payroll run updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        run = get_object_or_404(PayrollRun, pk=pk)
        serializer = PayrollRunSerializer(run, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_payroll_run(run, serializer.validated_data)
            return Response({"message": "Payroll run updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        run = get_object_or_404(PayrollRun, pk=pk)
        services.delete_payroll_run(run)
        return Response({"message": "Payroll run deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PAYSLIP VIEWSET
# ===========================================================================

class PayslipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        payslips = services.get_all_payslips()
        return Response(PayslipSerializer(payslips, many=True).data)

    def retrieve(self, request, pk=None):
        payslip = services.get_payslip_with_components(pk)
        return Response(PayslipSerializer(payslip).data)

    def create(self, request):
        serializer = PayslipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_payslip(serializer.validated_data)
            return Response({"message": "Payslip created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        payslip = get_object_or_404(Payslip, pk=pk)
        serializer = PayslipSerializer(payslip, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_payslip(payslip, serializer.validated_data)
            return Response({"message": "Payslip updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        payslip = get_object_or_404(Payslip, pk=pk)
        serializer = PayslipSerializer(payslip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_payslip(payslip, serializer.validated_data)
            return Response({"message": "Payslip updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        payslip = get_object_or_404(Payslip, pk=pk)
        services.delete_payslip(payslip)
        return Response({"message": "Payslip deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BONUS VIEWSET
# ===========================================================================

class BonusViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        bonuses = services.get_all_bonuses()
        return Response(BonusSerializer(bonuses, many=True).data)

    def retrieve(self, request, pk=None):
        bonus = get_object_or_404(Bonus, pk=pk)
        return Response(BonusSerializer(bonus).data)

    def create(self, request):
        serializer = BonusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bonus(serializer.validated_data)
            return Response({"message": "Bonus created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        bonus = get_object_or_404(Bonus, pk=pk)
        serializer = BonusSerializer(bonus, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bonus(bonus, serializer.validated_data)
            return Response({"message": "Bonus updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        bonus = get_object_or_404(Bonus, pk=pk)
        serializer = BonusSerializer(bonus, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bonus(bonus, serializer.validated_data)
            return Response({"message": "Bonus updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        bonus = get_object_or_404(Bonus, pk=pk)
        services.delete_bonus(bonus)
        return Response({"message": "Bonus deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PAYROLL DEDUCTION VIEWSET
# ===========================================================================

class PayrollDeductionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        deductions = services.get_all_deductions()
        return Response(PayrollDeductionSerializer(deductions, many=True).data)

    def retrieve(self, request, pk=None):
        deduction = get_object_or_404(PayrollDeduction, pk=pk)
        return Response(PayrollDeductionSerializer(deduction).data)

    def create(self, request):
        serializer = PayrollDeductionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_deduction(serializer.validated_data)
            return Response({"message": "Deduction created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        deduction = get_object_or_404(PayrollDeduction, pk=pk)
        serializer = PayrollDeductionSerializer(deduction, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_deduction(deduction, serializer.validated_data)
            return Response({"message": "Deduction updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        deduction = get_object_or_404(PayrollDeduction, pk=pk)
        serializer = PayrollDeductionSerializer(deduction, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_deduction(deduction, serializer.validated_data)
            return Response({"message": "Deduction updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        deduction = get_object_or_404(PayrollDeduction, pk=pk)
        services.delete_deduction(deduction)
        return Response({"message": "Deduction deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# LOAN VIEWSET
# ===========================================================================

class LoanViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        loans = services.get_all_loans()
        return Response(LoanSerializer(loans, many=True).data)

    def retrieve(self, request, pk=None):
        loan = services.get_loan_with_schedule(pk)
        return Response(LoanSerializer(loan).data)

    def create(self, request):
        serializer = LoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_loan(serializer.validated_data)
            return Response({"message": "Loan created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        loan = get_object_or_404(Loan, pk=pk)
        serializer = LoanSerializer(loan, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_loan(loan, serializer.validated_data)
            return Response({"message": "Loan updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        loan = get_object_or_404(Loan, pk=pk)
        serializer = LoanSerializer(loan, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_loan(loan, serializer.validated_data)
            return Response({"message": "Loan updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        loan = get_object_or_404(Loan, pk=pk)
        services.delete_loan(loan)
        return Response({"message": "Loan deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# STATUTORY FILING VIEWSET
# ===========================================================================

class StatutoryFilingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        filings = services.get_all_statutory_filings()
        return Response(StatutoryFilingSerializer(filings, many=True).data)

    def retrieve(self, request, pk=None):
        filing = get_object_or_404(StatutoryFiling, pk=pk)
        return Response(StatutoryFilingSerializer(filing).data)

    def create(self, request):
        serializer = StatutoryFilingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_statutory_filing(serializer.validated_data)
            return Response({"message": "Statutory filing created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        filing = get_object_or_404(StatutoryFiling, pk=pk)
        serializer = StatutoryFilingSerializer(filing, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_statutory_filing(filing, serializer.validated_data)
            return Response({"message": "Statutory filing updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        filing = get_object_or_404(StatutoryFiling, pk=pk)
        serializer = StatutoryFilingSerializer(filing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_statutory_filing(filing, serializer.validated_data)
            return Response({"message": "Statutory filing updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        filing = get_object_or_404(StatutoryFiling, pk=pk)
        services.delete_statutory_filing(filing)
        return Response({"message": "Statutory filing deleted successfully."}, status=status.HTTP_200_OK)
