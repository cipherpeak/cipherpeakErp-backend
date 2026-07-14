from django.contrib import admin
from .models import (
    Customer, PriceList, PriceListItem, SalesOrder, SOLine, Delivery, DeliveryLine,
    SalesInvoice, SalesInvoiceLine, SalesReturn, SalesReturnLine, CustomerPayment,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'name', 'contact_name', 'email', 'phone', 'city', 'country', 'credit_limit', 'outstanding_balance', 'payment_terms', 'status', 'created_at')
    search_fields = ('customer_number', 'name', 'email', 'trn')
    list_filter = ('status', 'payment_terms', 'industry')


class PriceListItemInline(admin.TabularInline):
    model = PriceListItem
    extra = 0


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'currency', 'status', 'is_default', 'valid_from', 'valid_to', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status', 'currency', 'is_default')
    inlines = [PriceListItemInline]


class SOLineInline(admin.TabularInline):
    model = SOLine
    extra = 0


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'status', 'payment_status', 'order_date', 'expected_delivery', 'currency', 'total', 'amount_paid', 'amount_due', 'created_at')
    search_fields = ('order_number', 'customer_name', 'quotation_ref')
    list_filter = ('status', 'payment_status', 'currency')
    inlines = [SOLineInline]


class DeliveryLineInline(admin.TabularInline):
    model = DeliveryLine
    extra = 0


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_number', 'order_number', 'customer_name', 'status', 'scheduled_date', 'shipped_date', 'delivered_date', 'carrier', 'tracking_number', 'created_at')
    search_fields = ('delivery_number', 'order_number', 'customer_name', 'tracking_number')
    list_filter = ('status', 'carrier')
    inlines = [DeliveryLineInline]


class SalesInvoiceLineInline(admin.TabularInline):
    model = SalesInvoiceLine
    extra = 0


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer_name', 'status', 'issue_date', 'due_date', 'currency', 'total', 'amount_paid', 'amount_due', 'created_at')
    search_fields = ('invoice_number', 'customer_name')
    list_filter = ('status', 'currency')
    inlines = [SalesInvoiceLineInline]


class SalesReturnLineInline(admin.TabularInline):
    model = SalesReturnLine
    extra = 0


@admin.register(SalesReturn)
class SalesReturnAdmin(admin.ModelAdmin):
    list_display = ('return_number', 'customer_name', 'status', 'reason', 'request_date', 'approved_date', 'received_date', 'refund_date', 'total_refund', 'created_at')
    search_fields = ('return_number', 'customer_name')
    list_filter = ('status',)
    inlines = [SalesReturnLineInline]


@admin.register(CustomerPayment)
class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'customer_name', 'invoice', 'amount', 'currency', 'payment_method', 'payment_date', 'status', 'created_at')
    search_fields = ('payment_number', 'customer_name', 'reference')
    list_filter = ('status', 'payment_method', 'currency')
