from rest_framework import serializers
from .models import (
    ItemCategory, Unit, Item, ItemSupplier, Warehouse, Bin, Stock,
    BatchRecord, SerialRecord, BarcodeRecord, StockAdjustment,
    StockTransfer, StockTransferItem, CycleCount, CycleCountItem,
    StockLedgerEntry, StockEntry,
)


# ===========================================================================
# CATEGORY SERIALIZER
# ===========================================================================

class ItemCategorySerializer(serializers.ModelSerializer):
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = ItemCategory
        fields = '__all__'

    def get_children_count(self, obj):
        return obj.children.filter(status='active').count()


# ===========================================================================
# UNIT SERIALIZER
# ===========================================================================

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


# ===========================================================================
# ITEM SERIALIZER
# ===========================================================================

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    unit_name_display = serializers.CharField(source='unit.symbol', read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


# ===========================================================================
# ITEM SUPPLIER SERIALIZER
# ===========================================================================

class ItemSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSupplier
        fields = '__all__'


# ===========================================================================
# WAREHOUSE SERIALIZER
# ===========================================================================

class WarehouseSerializer(serializers.ModelSerializer):
    bin_count = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = '__all__'

    def get_bin_count(self, obj):
        return obj.bins.filter(status='active').count()


# ===========================================================================
# BIN SERIALIZER
# ===========================================================================

class BinSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = Bin
        fields = '__all__'


# ===========================================================================
# STOCK SERIALIZER
# ===========================================================================

class StockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    available_qty = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


# ===========================================================================
# BATCH RECORD SERIALIZER
# ===========================================================================

class BatchRecordSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = BatchRecord
        fields = '__all__'


# ===========================================================================
# SERIAL RECORD SERIALIZER
# ===========================================================================

class SerialRecordSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = SerialRecord
        fields = '__all__'


# ===========================================================================
# BARCODE RECORD SERIALIZER
# ===========================================================================

class BarcodeRecordSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = BarcodeRecord
        fields = '__all__'


# ===========================================================================
# STOCK ADJUSTMENT SERIALIZER
# ===========================================================================

class StockAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAdjustment
        fields = '__all__'


# ===========================================================================
# STOCK TRANSFER SERIALIZER
# ===========================================================================

class StockTransferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransferItem
        fields = '__all__'


class StockTransferSerializer(serializers.ModelSerializer):
    transfer_items = StockTransferItemSerializer(many=True, read_only=True)

    class Meta:
        model = StockTransfer
        fields = '__all__'


# ===========================================================================
# CYCLE COUNT SERIALIZER
# ===========================================================================

class CycleCountItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CycleCountItem
        fields = '__all__'


class CycleCountSerializer(serializers.ModelSerializer):
    count_items = CycleCountItemSerializer(many=True, read_only=True)

    class Meta:
        model = CycleCount
        fields = '__all__'


# ===========================================================================
# STOCK LEDGER ENTRY SERIALIZER
# ===========================================================================

class StockLedgerEntrySerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = StockLedgerEntry
        fields = '__all__'


# ===========================================================================
# STOCK ENTRY SERIALIZER
# ===========================================================================

class StockEntrySerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = StockEntry
        fields = '__all__'
