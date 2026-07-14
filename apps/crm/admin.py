from django.contrib import admin
from .models import (
    Account, Contact, Lead, Opportunity, CRMActivity, CRMQuotation, CRMQuotationLine,
)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'name', 'industry', 'type', 'city', 'country', 'annual_revenue', 'assigned_to', 'status', 'created_at')
    search_fields = ('account_number', 'name', 'email', 'trn')
    list_filter = ('type', 'status', 'industry')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_name', 'position', 'department', 'email', 'phone', 'mobile', 'status', 'last_activity', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('status',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_number', 'name', 'company', 'email', 'phone', 'source', 'status', 'priority', 'assigned_to', 'score', 'estimated_value', 'created_at')
    search_fields = ('lead_number', 'name', 'company', 'email')
    list_filter = ('status', 'source', 'priority')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('opp_number', 'name', 'account_name', 'contact_name', 'stage', 'priority', 'value', 'probability', 'expected_close', 'assigned_to', 'created_at')
    search_fields = ('opp_number', 'name', 'account_name')
    list_filter = ('stage', 'priority')


@admin.register(CRMActivity)
class CRMActivityAdmin(admin.ModelAdmin):
    list_display = ('type', 'subject', 'status', 'related_to', 'related_id', 'assigned_to', 'due_date', 'done_date', 'created_at')
    search_fields = ('subject', 'description')
    list_filter = ('type', 'status', 'related_to')


class CRMQuotationLineInline(admin.TabularInline):
    model = CRMQuotationLine
    extra = 0


@admin.register(CRMQuotation)
class CRMQuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_number', 'account_name', 'contact_name', 'status', 'issue_date', 'expiry_date', 'currency', 'subtotal', 'total', 'assigned_to', 'created_at')
    search_fields = ('quotation_number', 'account_name')
    list_filter = ('status', 'currency')
    inlines = [CRMQuotationLineInline]


@admin.register(CRMQuotationLine)
class CRMQuotationLineAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'item_name', 'qty', 'unit_price', 'discount_pct', 'tax_pct', 'total')
    search_fields = ('item_name',)
