from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'price-lists', views.PriceListViewSet, basename='price-list')
router.register(r'sales-orders', views.SalesOrderViewSet, basename='sales-order')
router.register(r'deliveries', views.DeliveryViewSet, basename='delivery')
router.register(r'sales-invoices', views.SalesInvoiceViewSet, basename='sales-invoice')
router.register(r'sales-returns', views.SalesReturnViewSet, basename='sales-return')
router.register(r'customer-payments', views.CustomerPaymentViewSet, basename='customer-payment')

urlpatterns = [
    path('', include(router.urls)),
]
