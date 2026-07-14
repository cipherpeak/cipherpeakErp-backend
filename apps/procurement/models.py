from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CompanyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class VendorStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    BLOCKED = 'blocked', 'Blocked'


class PriorityLevel(models.TextChoices):
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


class POStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Submitted'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    SENT = 'sent', 'Sent'
    PARTIAL = 'partial', 'Partial'
    RECEIVED = 'received', 'Received'
    CANCELLED = 'cancelled', 'Cancelled'


class GRNStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    RECEIVED = 'received', 'Received'
    VERIFIED = 'verified', 'Verified'
    CANCELLED = 'cancelled', 'Cancelled'


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Cash'
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    CHEQUE = 'cheque', 'Cheque'
    ONLINE = 'online', 'Online'


# ---------------------------------------------------------------------------
# Vendor Category
# ---------------------------------------------------------------------------

class VendorCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    vendor_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vendor Category'
        verbose_name_plural = 'Vendor Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Payment Terms
# ---------------------------------------------------------------------------

class PaymentTerm(models.Model):
    name = models.CharField(max_length=100)
    days = models.IntegerField(help_text='0=immediate, 7, 15, 30, 45, 60')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    vendor_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Term'
        verbose_name_plural = 'Payment Terms'
        ordering = ['days']

    def __str__(self):
        return f"{self.name} ({self.days} days)"


# ---------------------------------------------------------------------------
# Vendor
# ---------------------------------------------------------------------------

class Vendor(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    gstin = models.CharField(max_length=50, blank=True, null=True)
    pan = models.CharField(max_length=50, blank=True, null=True)
    trn = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        VendorCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='vendors',
    )
    category_name = models.CharField(max_length=255, blank=True, null=True)
    payment_terms = models.ForeignKey(
        PaymentTerm, on_delete=models.SET_NULL, blank=True, null=True, related_name='vendors',
    )
    payment_terms_name = models.CharField(max_length=100, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rating = models.IntegerField(blank=True, null=True)
    is_preferred = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=VendorStatus.choices,
        default=VendorStatus.ACTIVE,
    )
    total_purchases = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_purchase_at = models.DateTimeField(blank=True, null=True)
    bank_account_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_branch = models.CharField(max_length=255, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=50, blank=True, null=True)
    bank_swift = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if self.category and not self.category_name:
            self.category_name = self.category.name
        if self.payment_terms and not self.payment_terms_name:
            self.payment_terms_name = self.payment_terms.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Vendor Contact
# ---------------------------------------------------------------------------

class VendorContact(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vendor Contact'
        verbose_name_plural = 'Vendor Contacts'
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f"{self.name} - {self.vendor.name}"


# ---------------------------------------------------------------------------
# Purchase Request
# ---------------------------------------------------------------------------

class PurchaseRequest(models.Model):
    pr_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    requested_by = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    priority = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices,
        default=PriorityLevel.NORMAL,
    )
    items = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, default='draft', help_text='draft/submitted/approved/rejected/fulfilled')
    total_estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Purchase Request'
        verbose_name_plural = 'Purchase Requests'
        ordering = ['-created_at']

    def __str__(self):
        return self.pr_number


# ---------------------------------------------------------------------------
# Purchase Request Item
# ---------------------------------------------------------------------------

class PurchaseRequestItem(models.Model):
    pr = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='pr_items')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    required_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Purchase Request Item'
        verbose_name_plural = 'Purchase Request Items'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# RFQ (Request for Quotation)
# ---------------------------------------------------------------------------

class RFQ(models.Model):
    rfq_number = models.CharField(max_length=50, unique=True)
    pr = models.ForeignKey(PurchaseRequest, on_delete=models.SET_NULL, blank=True, null=True, related_name='rfqs')
    pr_number = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='draft', help_text='draft/sent/closed/cancelled')
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'RFQ'
        verbose_name_plural = 'RFQs'
        ordering = ['-created_at']

    def __str__(self):
        return self.rfq_number

    def save(self, *args, **kwargs):
        if self.pr and not self.pr_number:
            self.pr_number = self.pr.pr_number
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# RFQ Vendor
# ---------------------------------------------------------------------------

class RFQVendor(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='rfq_vendors')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', help_text='pending/quoted/selected/rejected')

    class Meta:
        verbose_name = 'RFQ Vendor'
        verbose_name_plural = 'RFQ Vendors'

    def __str__(self):
        return f"{self.vendor_name} - {self.rfq.rfq_number}"

    def save(self, *args, **kwargs):
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# RFQ Item
# ---------------------------------------------------------------------------

class RFQItem(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='rfq_items')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'RFQ Item'
        verbose_name_plural = 'RFQ Items'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Quotation
# ---------------------------------------------------------------------------

class Quotation(models.Model):
    quotation_number = models.CharField(max_length=50, unique=True)
    rfq = models.ForeignKey(RFQ, on_delete=models.SET_NULL, blank=True, null=True, related_name='quotations')
    rfq_number = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='quotations')
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    valid_until = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_terms = models.CharField(max_length=255, blank=True, null=True)
    delivery_terms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='draft', help_text='draft/submitted/accepted/rejected')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotations'
        ordering = ['-created_at']

    def __str__(self):
        return self.quotation_number

    def save(self, *args, **kwargs):
        if self.rfq and not self.rfq_number:
            self.rfq_number = self.rfq.rfq_number
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Quotation Item
# ---------------------------------------------------------------------------

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='quotation_items')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Quotation Item'
        verbose_name_plural = 'Quotation Items'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Purchase Order
# ---------------------------------------------------------------------------

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    vendor_city = models.CharField(max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    payment_terms = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=POStatus.choices,
        default=POStatus.DRAFT,
    )
    remarks = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchase_orders')
    quotation_number = models.CharField(max_length=50, blank=True, null=True)
    pr = models.ForeignKey(PurchaseRequest, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchase_orders')
    pr_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.name
            self.vendor_city = self.vendor.city
        if self.quotation and not self.quotation_number:
            self.quotation_number = self.quotation.quotation_number
        if self.pr and not self.pr_number:
            self.pr_number = self.pr.pr_number
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Purchase Order Item
# ---------------------------------------------------------------------------

class PurchaseOrderItem(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='po_items')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# GRN (Goods Received Note)
# ---------------------------------------------------------------------------

class GRN(models.Model):
    grn_number = models.CharField(max_length=50, unique=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='grns')
    po_number = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True, related_name='grns')
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    warehouse = models.ForeignKey('inventory.Warehouse', on_delete=models.SET_NULL, blank=True, null=True, related_name='grns')
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    total_received_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=GRNStatus.choices,
        default=GRNStatus.DRAFT,
    )
    received_by = models.CharField(max_length=255, blank=True, null=True)
    verified_by = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    lr_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'GRN'
        verbose_name_plural = 'GRNs'
        ordering = ['-created_at']

    def __str__(self):
        return self.grn_number

    def save(self, *args, **kwargs):
        if self.po and not self.po_number:
            self.po_number = self.po.po_number
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.name
        if self.warehouse and not self.warehouse_name:
            self.warehouse_name = self.warehouse.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# GRN Item
# ---------------------------------------------------------------------------

class GRNItem(models.Model):
    grn = models.ForeignKey(GRN, on_delete=models.CASCADE, related_name='grn_items')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    ordered_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    received_qty = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'GRN Item'
        verbose_name_plural = 'GRN Items'

    def __str__(self):
        return f"{self.item_name} x {self.received_qty}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Purchase Invoice
# ---------------------------------------------------------------------------

class PurchaseInvoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoices')
    po_number = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoices')
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    invoice_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='draft', help_text='draft/validated/posted/paid')
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Purchase Invoice'
        verbose_name_plural = 'Purchase Invoices'
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if self.po and not self.po_number:
            self.po_number = self.po.po_number
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Purchase Invoice Item
# ---------------------------------------------------------------------------

class PurchaseInvoiceItem(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='invoice_items')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Purchase Invoice Item'
        verbose_name_plural = 'Purchase Invoice Items'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Vendor Payment
# ---------------------------------------------------------------------------

class VendorPayment(models.Model):
    payment_number = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.SET_NULL, blank=True, null=True, related_name='payments')
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payments')
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    reference = models.CharField(max_length=255, blank=True, null=True)
    bank_account = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', help_text='pending/completed/cancelled')
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vendor Payment'
        verbose_name_plural = 'Vendor Payments'
        ordering = ['-created_at']

    def __str__(self):
        return self.payment_number

    def save(self, *args, **kwargs):
        if self.invoice and not self.invoice_number:
            self.invoice_number = self.invoice.invoice_number
        if self.vendor and not self.vendor_name:
            self.vendor_name = self.vendor.name
        super().save(*args, **kwargs)
