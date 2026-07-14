from django.contrib import admin
from .models import (
    ItemCategory, Unit, Item, ItemSupplier, Warehouse, Bin, Stock,
    BatchRecord, SerialRecord, BarcodeRecord, StockAdjustment,
    StockTransfer, StockTransferItem, CycleCount, CycleCountItem,
    StockLedgerEntry, StockEntry,
)


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'level', 'item_count', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status', 'level')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'type', 'base_unit', 'conversion_factor', 'status', 'created_at')
    search_fields = ('name', 'symbol')
    list_filter = ('status', 'type')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'item_type', 'category_name', 'unit_name', 'current_stock', 'cost_price', 'selling_price', 'status', 'created_at')
    search_fields = ('name', 'sku', 'barcode')
    list_filter = ('status', 'item_type')


@admin.register(ItemSupplier)
class ItemSupplierAdmin(admin.ModelAdmin):
    list_display = ('item', 'vendor_id')
    search_fields = ('item__name',)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'manager', 'capacity_sqm', 'used_sqm', 'status', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('status',)


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ('code', 'warehouse', 'zone', 'row', 'rack', 'shelf', 'position', 'status', 'created_at')
    search_fields = ('code',)
    list_filter = ('status', 'warehouse')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('item', 'warehouse', 'bin', 'quantity', 'reserved_qty', 'last_updated')
    search_fields = ('item__name', 'warehouse__name')
    list_filter = ('warehouse',)


@admin.register(BatchRecord)
class BatchRecordAdmin(admin.ModelAdmin):
    list_display = ('item', 'batch_number', 'manufacturing_date', 'expiry_date', 'quantity', 'status', 'created_at')
    search_fields = ('batch_number',)
    list_filter = ('status',)


@admin.register(SerialRecord)
class SerialRecordAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'item', 'status', 'warehouse', 'created_at')
    search_fields = ('serial_number',)
    list_filter = ('status',)


@admin.register(BarcodeRecord)
class BarcodeRecordAdmin(admin.ModelAdmin):
    list_display = ('item', 'barcode', 'format', 'printed_date')
    search_fields = ('barcode',)


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('adjustment_number', 'item_name', 'item_sku', 'warehouse_name', 'adjustment_type', 'quantity', 'status', 'created_by', 'created_at')
    search_fields = ('adjustment_number', 'item_name', 'item_sku')
    list_filter = ('status', 'adjustment_type')


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_number', 'from_warehouse_name', 'to_warehouse_name', 'status', 'created_by', 'created_at')
    search_fields = ('transfer_number',)
    list_filter = ('status',)


@admin.register(StockTransferItem)
class StockTransferItemAdmin(admin.ModelAdmin):
    list_display = ('transfer', 'item', 'item_name', 'sku', 'quantity', 'unit_name')
    search_fields = ('item_name', 'sku')


@admin.register(CycleCount)
class CycleCountAdmin(admin.ModelAdmin):
    list_display = ('cycle_count_number', 'warehouse_name', 'status', 'counted_items', 'total_items', 'discrepancies', 'created_by', 'created_at')
    search_fields = ('cycle_count_number',)
    list_filter = ('status',)


@admin.register(CycleCountItem)
class CycleCountItemAdmin(admin.ModelAdmin):
    list_display = ('cycle_count', 'item', 'expected_qty', 'counted_qty', 'variance')
    search_fields = ('item__name',)


@admin.register(StockLedgerEntry)
class StockLedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'item', 'warehouse', 'description', 'debit_qty', 'credit_qty', 'balance_qty', 'reference', 'type')
    search_fields = ('reference',)
    list_filter = ('type',)


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ('item', 'warehouse', 'transaction_type', 'quantity', 'unit_cost', 'total_cost', 'reference_number', 'created_at')
    search_fields = ('reference_number',)
    list_filter = ('transaction_type',)
