from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'salary-structures', views.SalaryStructureViewSet, basename='salary-structure')
router.register(r'payroll-runs', views.PayrollRunViewSet, basename='payroll-run')
router.register(r'payslips', views.PayslipViewSet, basename='payslip')
router.register(r'bonuses', views.BonusViewSet, basename='bonus')
router.register(r'deductions', views.PayrollDeductionViewSet, basename='payroll-deduction')
router.register(r'loans', views.LoanViewSet, basename='loan')
router.register(r'statutory-filings', views.StatutoryFilingViewSet, basename='statutory-filing')

urlpatterns = [
    path('', include(router.urls)),
]
