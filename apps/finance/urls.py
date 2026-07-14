from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.ChartOfAccountViewSet, basename='account')
router.register(r'journals', views.JournalViewSet, basename='journal')
router.register(r'bank-accounts', views.BankAccountViewSet, basename='bank-account')
router.register(r'bank-transactions', views.BankTransactionViewSet, basename='bank-transaction')
router.register(r'bank-reconciliations', views.BankReconciliationViewSet, basename='bank-reconciliation')
router.register(r'budgets', views.BudgetViewSet, basename='budget')
router.register(r'fixed-assets', views.FixedAssetViewSet, basename='fixed-asset')
router.register(r'receivables', views.ReceivableViewSet, basename='receivable')

urlpatterns = [
    path('', include(router.urls)),
]
