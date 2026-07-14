from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.ItemCategoryViewSet, basename='item-category')
router.register(r'units', views.UnitViewSet, basename='unit')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'item-suppliers', views.ItemSupplierViewSet, basename='item-supplier')
router.register(r'warehouses', views.WarehouseViewSet, basename='warehouse')
router.register(r'bins', views.BinViewSet, basename='bin')
router.register(r'stocks', views.StockViewSet, basename='stock')
router.register(r'batch-records', views.BatchRecordViewSet, basename='batch-record')
router.register(r'serial-records', views.SerialRecordViewSet, basename='serial-record')
router.register(r'barcode-records', views.BarcodeRecordViewSet, basename='barcode-record')
router.register(r'adjustments', views.StockAdjustmentViewSet, basename='stock-adjustment')
router.register(r'transfers', views.StockTransferViewSet, basename='stock-transfer')
router.register(r'cycle-counts', views.CycleCountViewSet, basename='cycle-count')
router.register(r'ledger-entries', views.StockLedgerEntryViewSet, basename='stock-ledger-entry')
router.register(r'stock-entries', views.StockEntryViewSet, basename='stock-entry')

urlpatterns = [
    path('', include(router.urls)),
]
