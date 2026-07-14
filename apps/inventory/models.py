from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CompanyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class ItemType(models.TextChoices):
    RAW_MATERIAL = 'raw_material', 'Raw Material'
    FINISHED_GOOD = 'finished_good', 'Finished Good'
    SEMI_FINISHED = 'semi_finished', 'Semi-Finished'
    CONSUMABLE = 'consumable', 'Consumable'
    SERVICE = 'service', 'Service'


class ItemStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    DISCONTINUED = 'discontinued', 'Discontinued'


class AdjustmentType(models.TextChoices):
    ADDITION = 'addition', 'Addition'
    SUBTRACTION = 'subtraction', 'Subtraction'
    DAMAGE = 'damage', 'Damage'
    LOSS = 'loss', 'Loss'
    RETURN = 'return', 'Return'
    CORRECTION = 'correction', 'Correction'


class TransferStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    DISPATCHED = 'dispatched', 'Dispatched'
    RECEIVED = 'received', 'Received'
    CANCELLED = 'cancelled', 'Cancelled'


# ---------------------------------------------------------------------------
# Item Category
# ---------------------------------------------------------------------------

class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
    )
    level = models.IntegerField(default=1)
    path = models.CharField(max_length=500, blank=True, null=True)
    item_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item Category'
        verbose_name_plural = 'Item Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Unit
# ---------------------------------------------------------------------------

class Unit(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    type = models.CharField(max_length=50, blank=True, null=True, help_text='weight/volume/length/count/packaging')
    base_unit = models.CharField(max_length=50, blank=True, null=True)
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.symbol})"


# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------

class Item(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='items',
    )
    category_name = models.CharField(max_length=255, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='items',
    )
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    batch_tracking = models.BooleanField(default=False)
    serial_tracking = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"


# ---------------------------------------------------------------------------
# Item Supplier (M2M)
# ---------------------------------------------------------------------------

class ItemSupplier(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='suppliers')
    vendor_id = models.IntegerField()

    class Meta:
        verbose_name = 'Item Supplier'
        verbose_name_plural = 'Item Suppliers'
        unique_together = ['item', 'vendor_id']

    def __str__(self):
        return f"Item {self.item_id} - Vendor {self.vendor_id}"


# ---------------------------------------------------------------------------
# Warehouse
# ---------------------------------------------------------------------------

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    manager = models.CharField(max_length=255, blank=True, null=True)
    capacity_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    used_sqm = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


# ---------------------------------------------------------------------------
# Bin
# ---------------------------------------------------------------------------

class Bin(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='bins')
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=50, blank=True, null=True)
    row = models.CharField(max_length=20, blank=True, null=True)
    rack = models.CharField(max_length=20, blank=True, null=True)
    shelf = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bin'
        verbose_name_plural = 'Bins'
        ordering = ['code']

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.warehouse and not self.warehouse_name:
            self.warehouse_name = self.warehouse.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Stock
# ---------------------------------------------------------------------------

class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    bin = models.ForeignKey(Bin, on_delete=models.SET_NULL, blank=True, null=True, related_name='stocks')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reserved_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        unique_together = ['item', 'warehouse', 'bin']

    def __str__(self):
        return f"{self.item} @ {self.warehouse}"

    @property
    def available_qty(self):
        return self.quantity - self.reserved_qty


# ---------------------------------------------------------------------------
# Batch Record
# ---------------------------------------------------------------------------

class BatchRecord(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100)
    manufacturing_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='active', help_text='active/expired/consumed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Batch Record'
        verbose_name_plural = 'Batch Records'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item} - {self.batch_number}"


# ---------------------------------------------------------------------------
# Serial Record
# ---------------------------------------------------------------------------

class SerialRecord(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='serials')
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='available', help_text='available/in_stock/sold/scrapped')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, related_name='serials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Serial Record'
        verbose_name_plural = 'Serial Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.serial_number


# ---------------------------------------------------------------------------
# Barcode Record
# ---------------------------------------------------------------------------

class BarcodeRecord(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='barcodes')
    barcode = models.CharField(max_length=100)
    format = models.CharField(max_length=20, blank=True, null=True, help_text='EAN13/EAN8/UPC/QR/CODE128')
    printed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Barcode Record'
        verbose_name_plural = 'Barcode Records'

    def __str__(self):
        return f"{self.item} - {self.barcode}"


# ---------------------------------------------------------------------------
# Stock Adjustment
# ---------------------------------------------------------------------------

class StockAdjustment(models.Model):
    adjustment_number = models.CharField(max_length=50, unique=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='adjustments')
    item_name = models.CharField(max_length=255, blank=True, null=True)
    item_sku = models.CharField(max_length=100, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, related_name='adjustments')
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    adjustment_type = models.CharField(max_length=20, choices=AdjustmentType.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', help_text='pending/approved/rejected')
    created_by = models.CharField(max_length=255, blank=True, null=True)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    attachments = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stock Adjustment'
        verbose_name_plural = 'Stock Adjustments'
        ordering = ['-created_at']

    def __str__(self):
        return self.adjustment_number

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.item_sku = self.item.sku
        if self.warehouse and not self.warehouse_name:
            self.warehouse_name = self.warehouse.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Stock Transfer
# ---------------------------------------------------------------------------

class StockTransfer(models.Model):
    transfer_number = models.CharField(max_length=50, unique=True)
    from_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='outgoing_transfers',
    )
    from_warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    to_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='incoming_transfers',
    )
    to_warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    items = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TransferStatus.choices,
        default=TransferStatus.DRAFT,
    )
    remarks = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    dispatched_at = models.DateTimeField(blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stock Transfer'
        verbose_name_plural = 'Stock Transfers'
        ordering = ['-created_at']

    def __str__(self):
        return self.transfer_number

    def save(self, *args, **kwargs):
        if self.from_warehouse and not self.from_warehouse_name:
            self.from_warehouse_name = self.from_warehouse.name
        if self.to_warehouse and not self.to_warehouse_name:
            self.to_warehouse_name = self.to_warehouse.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Stock Transfer Item
# ---------------------------------------------------------------------------

class StockTransferItem(models.Model):
    transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='transfer_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Stock Transfer Item'
        verbose_name_plural = 'Stock Transfer Items'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Cycle Count
# ---------------------------------------------------------------------------

class CycleCount(models.Model):
    cycle_count_number = models.CharField(max_length=50, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, related_name='cycle_counts')
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='draft', help_text='draft/in_progress/completed/posted')
    counted_items = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    discrepancies = models.IntegerField(default=0)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cycle Count'
        verbose_name_plural = 'Cycle Counts'
        ordering = ['-created_at']

    def __str__(self):
        return self.cycle_count_number

    def save(self, *args, **kwargs):
        if self.warehouse and not self.warehouse_name:
            self.warehouse_name = self.warehouse.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Cycle Count Item
# ---------------------------------------------------------------------------

class CycleCountItem(models.Model):
    cycle_count = models.ForeignKey(CycleCount, on_delete=models.CASCADE, related_name='count_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    expected_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    counted_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    variance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Cycle Count Item'
        verbose_name_plural = 'Cycle Count Items'

    def __str__(self):
        return f"{self.item} - Count {self.cycle_count_id}"


# ---------------------------------------------------------------------------
# Stock Ledger Entry
# ---------------------------------------------------------------------------

class StockLedgerEntry(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='ledger_entries')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, related_name='ledger_entries')
    description = models.TextField(blank=True, null=True)
    debit_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stock Ledger Entry'
        verbose_name_plural = 'Stock Ledger Entries'
        ordering = ['-date']

    def __str__(self):
        return f"{self.item} - {self.date}"


# ---------------------------------------------------------------------------
# Stock Entry
# ---------------------------------------------------------------------------

class StockEntry(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_entries')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, related_name='stock_entries')
    transaction_type = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stock Entry'
        verbose_name_plural = 'Stock Entries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.item}"
