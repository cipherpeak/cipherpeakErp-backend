from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    ItemCategory, Unit, Item, ItemSupplier, Warehouse, Bin, Stock,
    BatchRecord, SerialRecord, BarcodeRecord, StockAdjustment,
    StockTransfer, StockTransferItem, CycleCount, CycleCountItem,
    StockLedgerEntry, StockEntry,
)
from .serializers import (
    ItemCategorySerializer, UnitSerializer, ItemSerializer, ItemSupplierSerializer,
    WarehouseSerializer, BinSerializer, StockSerializer,
    BatchRecordSerializer, SerialRecordSerializer, BarcodeRecordSerializer,
    StockAdjustmentSerializer, StockTransferSerializer, StockTransferItemSerializer,
    CycleCountSerializer, CycleCountItemSerializer,
    StockLedgerEntrySerializer, StockEntrySerializer,
)
from . import services


# ===========================================================================
# ITEM CATEGORY VIEWSET
# ===========================================================================

class ItemCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories = services.get_all_categories()
        serializer = ItemCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        node_type = request.query_params.get('type', 'category')
        if node_type == 'children':
            children = services.get_category_children(int(pk))
            serializer = ItemCategorySerializer(children, many=True)
            return Response(serializer.data)
        category = get_object_or_404(ItemCategory, pk=pk)
        serializer = ItemCategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_category(serializer.validated_data)
            return Response({"message": "Category created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = get_object_or_404(ItemCategory, pk=pk)
        serializer = ItemCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_category(category, serializer.validated_data)
            return Response({"message": "Category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = get_object_or_404(ItemCategory, pk=pk)
        serializer = ItemCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_category(category, serializer.validated_data)
            return Response({"message": "Category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = get_object_or_404(ItemCategory, pk=pk)
        services.delete_category(category)
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# UNIT VIEWSET
# ===========================================================================

class UnitViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        units = services.get_all_units()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        unit = get_object_or_404(Unit, pk=pk)
        serializer = UnitSerializer(unit)
        return Response(serializer.data)

    def create(self, request):
        serializer = UnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_unit(serializer.validated_data)
            return Response({"message": "Unit created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        unit = get_object_or_404(Unit, pk=pk)
        serializer = UnitSerializer(unit, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_unit(unit, serializer.validated_data)
            return Response({"message": "Unit updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        unit = get_object_or_404(Unit, pk=pk)
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_unit(unit, serializer.validated_data)
            return Response({"message": "Unit updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        unit = get_object_or_404(Unit, pk=pk)
        services.delete_unit(unit)
        return Response({"message": "Unit deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# ITEM VIEWSET
# ===========================================================================

class ItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = services.get_all_items()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_item(serializer.validated_data)
            return Response({"message": "Item created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_item(item, serializer.validated_data)
            return Response({"message": "Item updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_item(item, serializer.validated_data)
            return Response({"message": "Item updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        services.delete_item(item)
        return Response({"message": "Item deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# ITEM SUPPLIER VIEWSET
# ===========================================================================

class ItemSupplierViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        item_id = request.query_params.get('item_id')
        if item_id:
            suppliers = services.get_item_suppliers(int(item_id))
        else:
            suppliers = ItemSupplier.objects.all()
        serializer = ItemSupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemSupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_item_supplier(serializer.validated_data)
            return Response({"message": "Supplier linked successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        supplier = get_object_or_404(ItemSupplier, pk=pk)
        services.delete_item_supplier(supplier)
        return Response({"message": "Supplier unlinked successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# WAREHOUSE VIEWSET
# ===========================================================================

class WarehouseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        warehouses = services.get_all_warehouses()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = WarehouseSerializer(warehouse)
        return Response(serializer.data)

    def create(self, request):
        serializer = WarehouseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_warehouse(serializer.validated_data)
            return Response({"message": "Warehouse created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = WarehouseSerializer(warehouse, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_warehouse(warehouse, serializer.validated_data)
            return Response({"message": "Warehouse updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = WarehouseSerializer(warehouse, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_warehouse(warehouse, serializer.validated_data)
            return Response({"message": "Warehouse updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        services.delete_warehouse(warehouse)
        return Response({"message": "Warehouse deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BIN VIEWSET
# ===========================================================================

class BinViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        warehouse_id = request.query_params.get('warehouse_id')
        if warehouse_id:
            bins = services.get_bins_by_warehouse(int(warehouse_id))
        else:
            bins = services.get_all_bins()
        serializer = BinSerializer(bins, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        bin_obj = get_object_or_404(Bin, pk=pk)
        serializer = BinSerializer(bin_obj)
        return Response(serializer.data)

    def create(self, request):
        serializer = BinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bin(serializer.validated_data)
            return Response({"message": "Bin created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        bin_obj = get_object_or_404(Bin, pk=pk)
        serializer = BinSerializer(bin_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bin(bin_obj, serializer.validated_data)
            return Response({"message": "Bin updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        bin_obj = get_object_or_404(Bin, pk=pk)
        serializer = BinSerializer(bin_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bin(bin_obj, serializer.validated_data)
            return Response({"message": "Bin updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        bin_obj = get_object_or_404(Bin, pk=pk)
        services.delete_bin(bin_obj)
        return Response({"message": "Bin deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# STOCK VIEWSET
# ===========================================================================

class StockViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        warehouse_id = request.query_params.get('warehouse_id')
        if warehouse_id:
            stocks = services.get_stocks_by_warehouse(int(warehouse_id))
        else:
            stocks = services.get_all_stocks()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        stock = get_object_or_404(Stock, pk=pk)
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def create(self, request):
        serializer = StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_stock(serializer.validated_data)
            return Response({"message": "Stock created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        stock = get_object_or_404(Stock, pk=pk)
        serializer = StockSerializer(stock, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_stock(stock, serializer.validated_data)
            return Response({"message": "Stock updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        stock = get_object_or_404(Stock, pk=pk)
        serializer = StockSerializer(stock, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_stock(stock, serializer.validated_data)
            return Response({"message": "Stock updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        stock = get_object_or_404(Stock, pk=pk)
        services.delete_stock(stock)
        return Response({"message": "Stock deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BATCH RECORD VIEWSET
# ===========================================================================

class BatchRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        item_id = request.query_params.get('item_id')
        if item_id:
            batches = services.get_batch_records_by_item(int(item_id))
        else:
            batches = services.get_all_batch_records()
        serializer = BatchRecordSerializer(batches, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        batch = get_object_or_404(BatchRecord, pk=pk)
        serializer = BatchRecordSerializer(batch)
        return Response(serializer.data)

    def create(self, request):
        serializer = BatchRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_batch_record(serializer.validated_data)
            return Response({"message": "Batch record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        batch = get_object_or_404(BatchRecord, pk=pk)
        serializer = BatchRecordSerializer(batch, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_batch_record(batch, serializer.validated_data)
            return Response({"message": "Batch record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        batch = get_object_or_404(BatchRecord, pk=pk)
        serializer = BatchRecordSerializer(batch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_batch_record(batch, serializer.validated_data)
            return Response({"message": "Batch record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        batch = get_object_or_404(BatchRecord, pk=pk)
        services.delete_batch_record(batch)
        return Response({"message": "Batch record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SERIAL RECORD VIEWSET
# ===========================================================================

class SerialRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        item_id = request.query_params.get('item_id')
        if item_id:
            serials = services.get_serial_records_by_item(int(item_id))
        else:
            serials = services.get_all_serial_records()
        serializer = SerialRecordSerializer(serials, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serial = get_object_or_404(SerialRecord, pk=pk)
        serializer = SerialRecordSerializer(serial)
        return Response(serializer.data)

    def create(self, request):
        serializer = SerialRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_serial_record(serializer.validated_data)
            return Response({"message": "Serial record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serial = get_object_or_404(SerialRecord, pk=pk)
        serializer = SerialRecordSerializer(serial, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_serial_record(serial, serializer.validated_data)
            return Response({"message": "Serial record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        serial = get_object_or_404(SerialRecord, pk=pk)
        serializer = SerialRecordSerializer(serial, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_serial_record(serial, serializer.validated_data)
            return Response({"message": "Serial record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        serial = get_object_or_404(SerialRecord, pk=pk)
        services.delete_serial_record(serial)
        return Response({"message": "Serial record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BARCODE RECORD VIEWSET
# ===========================================================================

class BarcodeRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        item_id = request.query_params.get('item_id')
        if item_id:
            barcodes = services.get_barcodes_by_item(int(item_id))
        else:
            barcodes = services.get_all_barcodes()
        serializer = BarcodeRecordSerializer(barcodes, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BarcodeRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_barcode(serializer.validated_data)
            return Response({"message": "Barcode created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        barcode = get_object_or_404(BarcodeRecord, pk=pk)
        services.delete_barcode(barcode)
        return Response({"message": "Barcode deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# STOCK ADJUSTMENT VIEWSET
# ===========================================================================

class StockAdjustmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        adjustments = services.get_all_adjustments()
        serializer = StockAdjustmentSerializer(adjustments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment)
        return Response(serializer.data)

    def create(self, request):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_adjustment(serializer.validated_data)
            return Response({"message": "Adjustment created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_adjustment(adjustment, serializer.validated_data)
            return Response({"message": "Adjustment updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_adjustment(adjustment, serializer.validated_data)
            return Response({"message": "Adjustment updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        services.delete_adjustment(adjustment)
        return Response({"message": "Adjustment deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# STOCK TRANSFER VIEWSET
# ===========================================================================

class StockTransferViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        transfers = services.get_all_transfers()
        serializer = StockTransferSerializer(transfers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        transfer = services.get_transfer_with_items(pk)
        serializer = StockTransferSerializer(transfer)
        return Response(serializer.data)

    def create(self, request):
        serializer = StockTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_transfer(serializer.validated_data)
            return Response({"message": "Transfer created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        transfer = get_object_or_404(StockTransfer, pk=pk)
        serializer = StockTransferSerializer(transfer, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_transfer(transfer, serializer.validated_data)
            return Response({"message": "Transfer updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        transfer = get_object_or_404(StockTransfer, pk=pk)
        serializer = StockTransferSerializer(transfer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_transfer(transfer, serializer.validated_data)
            return Response({"message": "Transfer updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        transfer = get_object_or_404(StockTransfer, pk=pk)
        services.delete_transfer(transfer)
        return Response({"message": "Transfer deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CYCLE COUNT VIEWSET
# ===========================================================================

class CycleCountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cycle_counts = services.get_all_cycle_counts()
        serializer = CycleCountSerializer(cycle_counts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cycle_count = services.get_cycle_count_with_items(pk)
        serializer = CycleCountSerializer(cycle_count)
        return Response(serializer.data)

    def create(self, request):
        serializer = CycleCountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_cycle_count(serializer.validated_data)
            return Response({"message": "Cycle count created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        cycle_count = get_object_or_404(CycleCount, pk=pk)
        serializer = CycleCountSerializer(cycle_count, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_cycle_count(cycle_count, serializer.validated_data)
            return Response({"message": "Cycle count updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        cycle_count = get_object_or_404(CycleCount, pk=pk)
        serializer = CycleCountSerializer(cycle_count, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_cycle_count(cycle_count, serializer.validated_data)
            return Response({"message": "Cycle count updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cycle_count = get_object_or_404(CycleCount, pk=pk)
        services.delete_cycle_count(cycle_count)
        return Response({"message": "Cycle count deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# STOCK LEDGER ENTRY VIEWSET
# ===========================================================================

class StockLedgerEntryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        item_id = request.query_params.get('item_id')
        if item_id:
            entries = services.get_ledger_entries_by_item(int(item_id))
        else:
            entries = services.get_all_ledger_entries()
        serializer = StockLedgerEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        entry = get_object_or_404(StockLedgerEntry, pk=pk)
        serializer = StockLedgerEntrySerializer(entry)
        return Response(serializer.data)

    def create(self, request):
        serializer = StockLedgerEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_ledger_entry(serializer.validated_data)
            return Response({"message": "Ledger entry created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ===========================================================================
# STOCK ENTRY VIEWSET
# ===========================================================================

class StockEntryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        item_id = request.query_params.get('item_id')
        if item_id:
            entries = services.get_stock_entries_by_item(int(item_id))
        else:
            entries = services.get_all_stock_entries()
        serializer = StockEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        entry = get_object_or_404(StockEntry, pk=pk)
        serializer = StockEntrySerializer(entry)
        return Response(serializer.data)

    def create(self, request):
        serializer = StockEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_stock_entry(serializer.validated_data)
            return Response({"message": "Stock entry created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
