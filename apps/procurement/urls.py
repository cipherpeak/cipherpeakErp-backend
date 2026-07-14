from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vendor-categories', views.VendorCategoryViewSet, basename='vendor-category')
router.register(r'payment-terms', views.PaymentTermViewSet, basename='payment-term')
router.register(r'vendors', views.VendorViewSet, basename='vendor')
router.register(r'vendor-contacts', views.VendorContactViewSet, basename='vendor-contact')
router.register(r'purchase-requests', views.PurchaseRequestViewSet, basename='purchase-request')
router.register(r'rfqs', views.RFQViewSet, basename='rfq')
router.register(r'quotations', views.QuotationViewSet, basename='quotation')
router.register(r'purchase-orders', views.PurchaseOrderViewSet, basename='purchase-order')
router.register(r'grns', views.GRNViewSet, basename='grn')
router.register(r'purchase-invoices', views.PurchaseInvoiceViewSet, basename='purchase-invoice')
router.register(r'vendor-payments', views.VendorPaymentViewSet, basename='vendor-payment')

urlpatterns = [
    path('', include(router.urls)),
]
