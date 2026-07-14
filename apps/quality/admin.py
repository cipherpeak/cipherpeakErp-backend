from django.contrib import admin
from .models import (
    QualityCheck, DefectCategory, Inspection, InspectionChecklistItem,
    InspectionMeasurement, InspectionDefect, NCRRecord, CAPARecord, ReworkRecord,
)


@admin.register(QualityCheck)
class QualityCheckAdmin(admin.ModelAdmin):
    list_display = ('check_code', 'parameter', 'category', 'standard_value', 'tolerance', 'unit', 'frequency', 'status', 'created_at')
    search_fields = ('check_code', 'parameter')
    list_filter = ('category', 'frequency', 'status')
    filter_horizontal = ('products',)


@admin.register(DefectCategory)
class DefectCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'color', 'created_at')
    search_fields = ('code', 'name')


class InspectionChecklistItemInline(admin.TabularInline):
    model = InspectionChecklistItem
    extra = 0


class InspectionMeasurementInline(admin.TabularInline):
    model = InspectionMeasurement
    extra = 0


class InspectionDefectInline(admin.TabularInline):
    model = InspectionDefect
    extra = 0


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('inspection_number', 'wo_number', 'product_name', 'inspection_type', 'inspector_name', 'batch_number', 'accepted_qty', 'rejected_qty', 'status', 'date', 'created_at')
    search_fields = ('inspection_number', 'wo_number', 'product_name', 'batch_number')
    list_filter = ('inspection_type', 'status')
    inlines = [InspectionChecklistItemInline, InspectionMeasurementInline, InspectionDefectInline]


@admin.register(InspectionChecklistItem)
class InspectionChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('inspection', 'check_code', 'parameter', 'standard', 'actual_value', 'status')
    search_fields = ('check_code', 'parameter')
    list_filter = ('status',)


@admin.register(InspectionMeasurement)
class InspectionMeasurementAdmin(admin.ModelAdmin):
    list_display = ('inspection', 'parameter', 'unit', 'nominal', 'usl', 'lsl', 'mean_value', 'within_spec')
    search_fields = ('parameter',)
    list_filter = ('within_spec',)


@admin.register(InspectionDefect)
class InspectionDefectAdmin(admin.ModelAdmin):
    list_display = ('inspection', 'defect_code', 'defect_category', 'qty_defective', 'severity', 'location', 'disposition')
    search_fields = ('defect_code', 'description')
    list_filter = ('severity', 'disposition')


@admin.register(NCRRecord)
class NCRRecordAdmin(admin.ModelAdmin):
    list_display = ('ncr_number', 'product_name', 'severity', 'title', 'status', 'raised_by', 'assigned_to', 'closed_at', 'created_at')
    search_fields = ('ncr_number', 'title', 'product_name')
    list_filter = ('severity', 'status')


@admin.register(CAPARecord)
class CAPARecordAdmin(admin.ModelAdmin):
    list_display = ('capa_number', 'ncr', 'type', 'title', 'status', 'owner', 'target_date', 'verified_by', 'verified_at', 'created_at')
    search_fields = ('capa_number', 'title')
    list_filter = ('type', 'status')


@admin.register(ReworkRecord)
class ReworkRecordAdmin(admin.ModelAdmin):
    list_display = ('rework_number', 'ncr', 'wo', 'product_name', 'qty', 'status', 'assigned_to', 'started_at', 'completed_at', 'cost', 'created_at')
    search_fields = ('rework_number', 'product_name')
    list_filter = ('status',)
