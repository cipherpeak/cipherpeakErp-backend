from django.contrib import admin
from .models import (
    TaxJurisdiction, TaxType, HSNCode, TaxRate, TaxCategory,
    TaxGroup, TaxGroupMember, TaxRule, TaxRuleCondition,
    TaxExemption, ReverseChargeRecord, TaxReturn, TaxMappingRule,
)


@admin.register(TaxJurisdiction)
class TaxJurisdictionAdmin(admin.ModelAdmin):
    list_display = ('country', 'country_code', 'authority', 'currency_code', 'filing_frequency', 'next_due', 'status', 'created_at')
    search_fields = ('country', 'authority', 'registration_number')
    list_filter = ('status', 'filing_frequency')


@admin.register(TaxType)
class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'applicable_to', 'jurisdiction', 'rate_type', 'default_rate', 'status', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status', 'rate_type')


@admin.register(HSNCode)
class HSNCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'chapter', 'chapter_name', 'tax_rate', 'sac_code', 'status', 'created_at')
    search_fields = ('code', 'chapter_name', 'sac_code')
    list_filter = ('status',)


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'tax_type', 'jurisdiction', 'rate', 'rate_type', 'effective_from', 'effective_to', 'priority', 'status', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status', 'rate_type')


@admin.register(TaxCategory)
class TaxCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'default_rate', 'hsn_count', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('type', 'status')


class TaxGroupMemberInline(admin.TabularInline):
    model = TaxGroupMember
    extra = 0


@admin.register(TaxGroup)
class TaxGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'jurisdiction', 'composite_rate', 'applicability', 'status', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status',)
    inlines = [TaxGroupMemberInline]


class TaxRuleConditionInline(admin.TabularInline):
    model = TaxRuleCondition
    extra = 0


@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'jurisdiction', 'priority', 'action_type', 'action_rate', 'module', 'usage_count', 'status', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status', 'action_type')
    inlines = [TaxRuleConditionInline]


@admin.register(TaxExemption)
class TaxExemptionAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'holder_name', 'holder_type', 'exemption_type', 'percentage', 'valid_from', 'valid_to', 'status', 'created_at')
    search_fields = ('certificate_number', 'holder_name', 'gstin')
    list_filter = ('exemption_type', 'status')


@admin.register(ReverseChargeRecord)
class ReverseChargeRecordAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'vendor', 'invoice_date', 'invoice_amount', 'tax_amount', 'tax_type', 'is_rcm', 'payment_status', 'status', 'created_at')
    search_fields = ('invoice_number', 'vendor_gstin')
    list_filter = ('status', 'is_rcm', 'payment_status')


@admin.register(TaxReturn)
class TaxReturnAdmin(admin.ModelAdmin):
    list_display = ('return_type', 'form_name', 'period', 'filing_due_date', 'filed_date', 'tax_payable', 'tax_paid', 'status', 'created_at')
    search_fields = ('return_type', 'period', 'arn')
    list_filter = ('status', 'return_type')


@admin.register(TaxMappingRule)
class TaxMappingRuleAdmin(admin.ModelAdmin):
    list_display = ('source_jurisdiction', 'target_jurisdiction', 'source_field', 'target_field', 'source_rate', 'target_rate', 'mapping_type', 'status', 'created_at')
    search_fields = ('source_field', 'target_field', 'mapping_type')
    list_filter = ('status',)
