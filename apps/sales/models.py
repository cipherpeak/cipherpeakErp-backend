from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CurrencyCode(models.TextChoices):
    AED = 'AED', 'AED'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    INR = 'INR', 'INR'
    SAR = 'SAR', 'SAR'


class CustomerStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    BLOCKED = 'blocked', 'Blocked'


class PaymentTerms(models.TextChoices):
    IMMEDIATE = 'immediate', 'Immediate'
    NET_15 = 'net_15', 'Net 15'
    NET_30 = 'net_30', 'Net 30'
    NET_45 = 'net_45', 'Net 45'
    NET_60 = 'net_60', 'Net 60'
    NET_90 = 'net_90', 'Net 90'


class SOStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    CONFIRMED = 'confirmed', 'Confirmed'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'


class SOPaymentStatus(models.TextChoices):
    UNPAID = 'unpaid', 'Unpaid'
    PARTIAL = 'partial', 'Partial'
    PAID = 'paid', 'Paid'


class DeliveryStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    DISPATCHED = 'dispatched', 'Dispatched'
    IN_TRANSIT = 'in_transit', 'In Transit'
    DELIVERED = 'delivered', 'Delivered'
    FAILED = 'failed', 'Failed'


class SalesInvoiceStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SENT = 'sent', 'Sent'
    PARTIALLY_PAID = 'partially_paid', 'Partially Paid'
    PAID = 'paid', 'Paid'
    OVERDUE = 'overdue', 'Overdue'
    CANCELLED = 'cancelled', 'Cancelled'


class SalesReturnStatus(models.TextChoices):
    REQUESTED = 'requested', 'Requested'
    APPROVED = 'approved', 'Approved'
    RECEIVED = 'received', 'Received'
    REFUNDED = 'refunded', 'Refunded'
    REJECTED = 'rejected', 'Rejected'


class PriceListStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DRAFT = 'draft', 'Draft'
    EXPIRED = 'expired', 'Expired'


class CustPayMethod(models.TextChoices):
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    CHEQUE = 'cheque', 'Cheque'
    CASH = 'cash', 'Cash'
    CREDIT_CARD = 'credit_card', 'Credit Card'
    ONLINE = 'online', 'Online'
    CREDIT_NOTE = 'credit_note', 'Credit Note'


class CustPayStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CLEARED = 'cleared', 'Cleared'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------

class Customer(models.Model):
    customer_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    account = models.ForeignKey(
        'crm.Account', on_delete=models.SET_NULL, blank=True, null=True, related_name='customers',
    )
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    mobile = models.CharField(max_length=40, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    trn = models.CharField(max_length=30, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    payment_terms = models.CharField(
        max_length=20,
        choices=PaymentTerms.choices,
        default=PaymentTerms.NET_30,
    )
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='customers',
    )
    status = models.CharField(
        max_length=20,
        choices=CustomerStatus.choices,
        default=CustomerStatus.ACTIVE,
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['name']

    def __str__(self):
        return f"{self.customer_number} - {self.name}"


# ---------------------------------------------------------------------------
# Price List
# ---------------------------------------------------------------------------

class PriceList(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    status = models.CharField(
        max_length=20,
        choices=PriceListStatus.choices,
        default=PriceListStatus.DRAFT,
    )
    is_default = models.BooleanField(default=False)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    applicable_to = models.CharField(max_length=120, blank=True, null=True)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_price_lists',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Price List'
        verbose_name_plural = 'Price Lists'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class PriceListItem(models.Model):
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(
        'inventory.Item', on_delete=models.SET_NULL, blank=True, null=True, related_name='price_list_items',
    )
    item_code = models.CharField(max_length=60, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    base_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    list_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)

    class Meta:
        verbose_name = 'Price List Item'
        verbose_name_plural = 'Price List Items'

    def __str__(self):
        return f"{self.price_list.code} - {self.item_name}"


# ---------------------------------------------------------------------------
# Sales Order
# ---------------------------------------------------------------------------

class SalesOrder(models.Model):
    order_number = models.CharField(max_length=40, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales_orders')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    quotation_ref = models.CharField(max_length=40, blank=True, null=True)
    opportunity_ref = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=SOStatus.choices,
        default=SOStatus.DRAFT,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=SOPaymentStatus.choices,
        default=SOPaymentStatus.UNPAID,
    )
    payment_terms = models.CharField(max_length=60, blank=True, null=True)
    order_date = models.DateField()
    expected_delivery = models.DateField(blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    price_list = models.ForeignKey(
        PriceList, on_delete=models.SET_NULL, blank=True, null=True, related_name='sales_orders',
    )
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales_orders',
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if self.customer and not self.customer_name:
            self.customer_name = self.customer.name
        super().save(*args, **kwargs)


class SOLine(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey(
        'inventory.Item', on_delete=models.SET_NULL, blank=True, null=True, related_name='so_lines',
    )
    item_code = models.CharField(max_length=60, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    qty = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        verbose_name = 'Sales Order Line'
        verbose_name_plural = 'Sales Order Lines'

    def __str__(self):
        return f"{self.sales_order.order_number} - {self.item_name}"


# ---------------------------------------------------------------------------
# Delivery
# ---------------------------------------------------------------------------

class Delivery(models.Model):
    delivery_number = models.CharField(max_length=40, unique=True)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.PROTECT, related_name='deliveries')
    order_number = models.CharField(max_length=40, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='deliveries')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
    )
    scheduled_date = models.DateField(blank=True, null=True)
    shipped_date = models.DateField(blank=True, null=True)
    delivered_date = models.DateField(blank=True, null=True)
    carrier = models.CharField(max_length=120, blank=True, null=True)
    tracking_number = models.CharField(max_length=80, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
        ordering = ['-created_at']

    def __str__(self):
        return self.delivery_number

    def save(self, *args, **kwargs):
        if self.sales_order and not self.order_number:
            self.order_number = self.sales_order.order_number
        if self.customer and not self.customer_name:
            self.customer_name = self.customer.name
        super().save(*args, **kwargs)


class DeliveryLine(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey(
        'inventory.Item', on_delete=models.SET_NULL, blank=True, null=True, related_name='delivery_lines',
    )
    item_code = models.CharField(max_length=60, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    ordered_qty = models.DecimalField(max_digits=14, decimal_places=3)
    delivered_qty = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    class Meta:
        verbose_name = 'Delivery Line'
        verbose_name_plural = 'Delivery Lines'

    def __str__(self):
        return f"{self.delivery.delivery_number} - {self.item_name}"


# ---------------------------------------------------------------------------
# Sales Invoice
# ---------------------------------------------------------------------------

class SalesInvoice(models.Model):
    invoice_number = models.CharField(max_length=40, unique=True)
    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoices',
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=SalesInvoiceStatus.choices,
        default=SalesInvoiceStatus.DRAFT,
    )
    issue_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    payment_terms = models.CharField(max_length=60, blank=True, null=True)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales_invoices',
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sales Invoice'
        verbose_name_plural = 'Sales Invoices'
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if self.customer and not self.customer_name:
            self.customer_name = self.customer.name
        super().save(*args, **kwargs)


class SalesInvoiceLine(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey(
        'inventory.Item', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales_invoice_lines',
    )
    item_code = models.CharField(max_length=60, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    qty = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        verbose_name = 'Sales Invoice Line'
        verbose_name_plural = 'Sales Invoice Lines'

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.item_name}"


# ---------------------------------------------------------------------------
# Sales Return
# ---------------------------------------------------------------------------

class SalesReturn(models.Model):
    return_number = models.CharField(max_length=40, unique=True)
    invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.SET_NULL, blank=True, null=True, related_name='returns',
    )
    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.SET_NULL, blank=True, null=True, related_name='returns',
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='returns')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=SalesReturnStatus.choices,
        default=SalesReturnStatus.REQUESTED,
    )
    reason = models.CharField(max_length=60, blank=True, null=True)
    reason_detail = models.TextField(blank=True, null=True)
    request_date = models.DateField()
    approved_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    refund_date = models.DateField(blank=True, null=True)
    total_refund = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    refund_method = models.CharField(max_length=60, blank=True, null=True)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales_returns',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sales Return'
        verbose_name_plural = 'Sales Returns'
        ordering = ['-created_at']

    def __str__(self):
        return self.return_number

    def save(self, *args, **kwargs):
        if self.customer and not self.customer_name:
            self.customer_name = self.customer.name
        super().save(*args, **kwargs)


class SalesReturnLine(models.Model):
    sales_return = models.ForeignKey(SalesReturn, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey(
        'inventory.Item', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales_return_lines',
    )
    item_code = models.CharField(max_length=60, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    qty_returned = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        verbose_name = 'Sales Return Line'
        verbose_name_plural = 'Sales Return Lines'

    def __str__(self):
        return f"{self.sales_return.return_number} - {self.item_name}"


# ---------------------------------------------------------------------------
# Customer Payment
# ---------------------------------------------------------------------------

class CustomerPayment(models.Model):
    payment_number = models.CharField(max_length=40, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='payments')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.SET_NULL, blank=True, null=True, related_name='payments',
    )
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    payment_method = models.CharField(max_length=20, choices=CustPayMethod.choices)
    payment_date = models.DateField()
    value_date = models.DateField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=120, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CustPayStatus.choices,
        default=CustPayStatus.PENDING,
    )
    received_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='received_payments',
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Customer Payment'
        verbose_name_plural = 'Customer Payments'
        ordering = ['-created_at']

    def __str__(self):
        return self.payment_number

    def save(self, *args, **kwargs):
        if self.customer and not self.customer_name:
            self.customer_name = self.customer.name
        super().save(*args, **kwargs)
