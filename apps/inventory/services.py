from django.db import transaction
from typing import Dict, Any, List
from .models import (
    ItemCategory, Unit, Item, ItemSupplier, Warehouse, Bin, Stock,
    BatchRecord, SerialRecord, BarcodeRecord, StockAdjustment,
    StockTransfer, StockTransferItem, CycleCount, CycleCountItem,
    StockLedgerEntry, StockEntry, CompanyStatus,
)


# ===========================================================================
# ITEM CATEGORY SERVICES
# ===========================================================================

def get_all_categories() -> List[ItemCategory]:
    return ItemCategory.objects.filter(parent__isnull=True)

def get_category_children(category_id: int) -> List[ItemCategory]:
    return ItemCategory.objects.filter(parent_id=category_id, status='active')

def create_category(data: Dict[str, Any]) -> ItemCategory:
    name = data.get('name')
    if ItemCategory.objects.filter(name__iexact=name, parent=data.get('parent')).exists():
        raise ValueError(f"Category with name '{name}' already exists under this parent.")
    category = ItemCategory.objects.create(**data)
    if category.parent:
        category.level = category.parent.level + 1
        category.path = f"{category.parent.path}/{category.id}"
        category.save()
    else:
        category.level = 1
        category.path = f"/{category.id}"
        category.save()
    return category

def update_category(category: ItemCategory, data: Dict[str, Any]) -> ItemCategory:
    name = data.get('name')
    if name and ItemCategory.objects.filter(name__iexact=name, parent=category.parent).exclude(id=category.id).exists():
        raise ValueError(f"Category with name '{name}' already exists under this parent.")
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete_category(category: ItemCategory) -> None:
    category.delete()


# ===========================================================================
# UNIT SERVICES
# ===========================================================================

def get_all_units() -> List[Unit]:
    return Unit.objects.all()

def create_unit(data: Dict[str, Any]) -> Unit:
    name = data.get('name')
    if Unit.objects.filter(name__iexact=name).exists():
        raise ValueError(f"Unit with name '{name}' already exists.")
    return Unit.objects.create(**data)

def update_unit(unit: Unit, data: Dict[str, Any]) -> Unit:
    name = data.get('name')
    if name and Unit.objects.filter(name__iexact=name).exclude(id=unit.id).exists():
        raise ValueError(f"Unit with name '{name}' already exists.")
    for field, value in data.items():
        setattr(unit, field, value)
    unit.save()
    return unit

def delete_unit(unit: Unit) -> None:
    unit.delete()


# ===========================================================================
# ITEM SERVICES
# ===========================================================================

def get_all_items() -> List[Item]:
    return Item.objects.all()

def create_item(data: Dict[str, Any]) -> Item:
    sku = data.get('sku')
    if Item.objects.filter(sku__iexact=sku).exists():
        raise ValueError(f"Item with SKU '{sku}' already exists.")
    return Item.objects.create(**data)

def update_item(item: Item, data: Dict[str, Any]) -> Item:
    sku = data.get('sku')
    if sku and Item.objects.filter(sku__iexact=sku).exclude(id=item.id).exists():
        raise ValueError(f"Item with SKU '{sku}' already exists.")
    for field, value in data.items():
        setattr(item, field, value)
    item.save()
    return item

def delete_item(item: Item) -> None:
    item.delete()


# ===========================================================================
# ITEM SUPPLIER SERVICES
# ===========================================================================

def get_item_suppliers(item_id: int) -> List[ItemSupplier]:
    return ItemSupplier.objects.filter(item_id=item_id)

def create_item_supplier(data: Dict[str, Any]) -> ItemSupplier:
    if ItemSupplier.objects.filter(item_id=data.get('item_id'), vendor_id=data.get('vendor_id')).exists():
        raise ValueError("Supplier already linked to this item.")
    return ItemSupplier.objects.create(**data)

def delete_item_supplier(supplier: ItemSupplier) -> None:
    supplier.delete()


# ===========================================================================
# WAREHOUSE SERVICES
# ===========================================================================

def get_all_warehouses() -> List[Warehouse]:
    return Warehouse.objects.all()

def create_warehouse(data: Dict[str, Any]) -> Warehouse:
    code = data.get('code')
    if Warehouse.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Warehouse with code '{code}' already exists.")
    return Warehouse.objects.create(**data)

def update_warehouse(warehouse: Warehouse, data: Dict[str, Any]) -> Warehouse:
    code = data.get('code')
    if code and Warehouse.objects.filter(code__iexact=code).exclude(id=warehouse.id).exists():
        raise ValueError(f"Warehouse with code '{code}' already exists.")
    for field, value in data.items():
        setattr(warehouse, field, value)
    warehouse.save()
    return warehouse

def delete_warehouse(warehouse: Warehouse) -> None:
    warehouse.delete()


# ===========================================================================
# BIN SERVICES
# ===========================================================================

def get_all_bins() -> List[Bin]:
    return Bin.objects.all()

def get_bins_by_warehouse(warehouse_id: int) -> List[Bin]:
    return Bin.objects.filter(warehouse_id=warehouse_id, status='active')

def create_bin(data: Dict[str, Any]) -> Bin:
    code = data.get('code')
    if Bin.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Bin with code '{code}' already exists.")
    return Bin.objects.create(**data)

def update_bin(bin_obj: Bin, data: Dict[str, Any]) -> Bin:
    code = data.get('code')
    if code and Bin.objects.filter(code__iexact=code).exclude(id=bin_obj.id).exists():
        raise ValueError(f"Bin with code '{code}' already exists.")
    for field, value in data.items():
        setattr(bin_obj, field, value)
    bin_obj.save()
    return bin_obj

def delete_bin(bin_obj: Bin) -> None:
    bin_obj.delete()


# ===========================================================================
# STOCK SERVICES
# ===========================================================================

def get_all_stocks() -> List[Stock]:
    return Stock.objects.select_related('item', 'warehouse', 'bin').all()

def get_stocks_by_warehouse(warehouse_id: int) -> List[Stock]:
    return Stock.objects.filter(warehouse_id=warehouse_id).select_related('item')

def create_stock(data: Dict[str, Any]) -> Stock:
    return Stock.objects.create(**data)

def update_stock(stock: Stock, data: Dict[str, Any]) -> Stock:
    for field, value in data.items():
        setattr(stock, field, value)
    stock.save()
    return stock

def delete_stock(stock: Stock) -> None:
    stock.delete()


# ===========================================================================
# BATCH RECORD SERVICES
# ===========================================================================

def get_all_batch_records() -> List[BatchRecord]:
    return BatchRecord.objects.select_related('item').all()

def get_batch_records_by_item(item_id: int) -> List[BatchRecord]:
    return BatchRecord.objects.filter(item_id=item_id)

def create_batch_record(data: Dict[str, Any]) -> BatchRecord:
    return BatchRecord.objects.create(**data)

def update_batch_record(batch: BatchRecord, data: Dict[str, Any]) -> BatchRecord:
    for field, value in data.items():
        setattr(batch, field, value)
    batch.save()
    return batch

def delete_batch_record(batch: BatchRecord) -> None:
    batch.delete()


# ===========================================================================
# SERIAL RECORD SERVICES
# ===========================================================================

def get_all_serial_records() -> List[SerialRecord]:
    return SerialRecord.objects.select_related('item', 'warehouse').all()

def get_serial_records_by_item(item_id: int) -> List[SerialRecord]:
    return SerialRecord.objects.filter(item_id=item_id)

def create_serial_record(data: Dict[str, Any]) -> SerialRecord:
    serial_number = data.get('serial_number')
    if SerialRecord.objects.filter(serial_number__iexact=serial_number).exists():
        raise ValueError(f"Serial number '{serial_number}' already exists.")
    return SerialRecord.objects.create(**data)

def update_serial_record(serial: SerialRecord, data: Dict[str, Any]) -> SerialRecord:
    for field, value in data.items():
        setattr(serial, field, value)
    serial.save()
    return serial

def delete_serial_record(serial: SerialRecord) -> None:
    serial.delete()


# ===========================================================================
# BARCODE RECORD SERVICES
# ===========================================================================

def get_all_barcodes() -> List[BarcodeRecord]:
    return BarcodeRecord.objects.select_related('item').all()

def get_barcodes_by_item(item_id: int) -> List[BarcodeRecord]:
    return BarcodeRecord.objects.filter(item_id=item_id)

def create_barcode(data: Dict[str, Any]) -> BarcodeRecord:
    return BarcodeRecord.objects.create(**data)

def delete_barcode(barcode: BarcodeRecord) -> None:
    barcode.delete()


# ===========================================================================
# STOCK ADJUSTMENT SERVICES
# ===========================================================================

def get_all_adjustments() -> List[StockAdjustment]:
    return StockAdjustment.objects.select_related('item', 'warehouse').all()

def create_adjustment(data: Dict[str, Any]) -> StockAdjustment:
    adjustment_number = data.get('adjustment_number')
    if StockAdjustment.objects.filter(adjustment_number__iexact=adjustment_number).exists():
        raise ValueError(f"Adjustment number '{adjustment_number}' already exists.")
    return StockAdjustment.objects.create(**data)

def update_adjustment(adjustment: StockAdjustment, data: Dict[str, Any]) -> StockAdjustment:
    for field, value in data.items():
        setattr(adjustment, field, value)
    adjustment.save()
    return adjustment

def delete_adjustment(adjustment: StockAdjustment) -> None:
    adjustment.delete()


# ===========================================================================
# STOCK TRANSFER SERVICES
# ===========================================================================

def get_all_transfers() -> List[StockTransfer]:
    return StockTransfer.objects.all()

def get_transfer_with_items(transfer_id: int) -> StockTransfer:
    return StockTransfer.objects.prefetch_related('transfer_items').get(pk=transfer_id)

def create_transfer(data: Dict[str, Any]) -> StockTransfer:
    transfer_number = data.get('transfer_number')
    if StockTransfer.objects.filter(transfer_number__iexact=transfer_number).exists():
        raise ValueError(f"Transfer number '{transfer_number}' already exists.")
    items_data = data.pop('items', [])
    transfer = StockTransfer.objects.create(**data)
    for item_data in items_data:
        StockTransferItem.objects.create(transfer=transfer, **item_data)
    return transfer

def update_transfer(transfer: StockTransfer, data: Dict[str, Any]) -> StockTransfer:
    for field, value in data.items():
        setattr(transfer, field, value)
    transfer.save()
    return transfer

def delete_transfer(transfer: StockTransfer) -> None:
    transfer.delete()


# ===========================================================================
# CYCLE COUNT SERVICES
# ===========================================================================

def get_all_cycle_counts() -> List[CycleCount]:
    return CycleCount.objects.all()

def get_cycle_count_with_items(cycle_count_id: int) -> CycleCount:
    return CycleCount.objects.prefetch_related('count_items').get(pk=cycle_count_id)

def create_cycle_count(data: Dict[str, Any]) -> CycleCount:
    cycle_count_number = data.get('cycle_count_number')
    if CycleCount.objects.filter(cycle_count_number__iexact=cycle_count_number).exists():
        raise ValueError(f"Cycle count number '{cycle_count_number}' already exists.")
    items_data = data.pop('items', [])
    cycle_count = CycleCount.objects.create(**data)
    for item_data in items_data:
        CycleCountItem.objects.create(cycle_count=cycle_count, **item_data)
    return cycle_count

def update_cycle_count(cycle_count: CycleCount, data: Dict[str, Any]) -> CycleCount:
    for field, value in data.items():
        setattr(cycle_count, field, value)
    cycle_count.save()
    return cycle_count

def delete_cycle_count(cycle_count: CycleCount) -> None:
    cycle_count.delete()


# ===========================================================================
# STOCK LEDGER ENTRY SERVICES
# ===========================================================================

def get_all_ledger_entries() -> List[StockLedgerEntry]:
    return StockLedgerEntry.objects.select_related('item', 'warehouse').all()

def get_ledger_entries_by_item(item_id: int) -> List[StockLedgerEntry]:
    return StockLedgerEntry.objects.filter(item_id=item_id)

def create_ledger_entry(data: Dict[str, Any]) -> StockLedgerEntry:
    return StockLedgerEntry.objects.create(**data)


# ===========================================================================
# STOCK ENTRY SERVICES
# ===========================================================================

def get_all_stock_entries() -> List[StockEntry]:
    return StockEntry.objects.select_related('item', 'warehouse').all()

def get_stock_entries_by_item(item_id: int) -> List[StockEntry]:
    return StockEntry.objects.filter(item_id=item_id)

def create_stock_entry(data: Dict[str, Any]) -> StockEntry:
    return StockEntry.objects.create(**data)
