from django.contrib import admin
from .models import (
    KPI, KPIHistory, KPIAlert, Dashboard, DashboardWidget, Report, SavedReport,
    ScheduledReport, ForecastSeries, ForecastPoint, Anomaly, Recommendation,
    Scenario, AIConversation, AIMessage, ExportJob,
)


class KPIHistoryInline(admin.TabularInline):
    model = KPIHistory
    extra = 0


class KPIAlertInline(admin.TabularInline):
    model = KPIAlert
    extra = 0


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'owner', 'value', 'target', 'change_pct', 'trend', 'status', 'frequency', 'last_updated')
    search_fields = ('name', 'module', 'owner')
    list_filter = ('status', 'trend', 'frequency')
    inlines = [KPIHistoryInline, KPIAlertInline]


class DashboardWidgetInline(admin.TabularInline):
    model = DashboardWidget
    extra = 0


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'is_shared', 'created_by', 'last_viewed', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_default', 'is_shared')
    inlines = [DashboardWidgetInline]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'status', 'chart_type', 'row_count', 'is_scheduled', 'created_by', 'last_run', 'created_at')
    search_fields = ('name', 'module')
    list_filter = ('status', 'is_scheduled')


@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'module', 'snapshot_date', 'row_count', 'file_size_kb', 'format', 'generated_by', 'expires_at')
    search_fields = ('report_name', 'module')
    list_filter = ('format',)


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'module', 'frequency', 'run_time', 'format', 'last_run', 'last_run_status', 'next_run', 'status', 'created_at')
    search_fields = ('report_name', 'module')
    list_filter = ('frequency', 'status', 'format')


class ForecastPointInline(admin.TabularInline):
    model = ForecastPoint
    extra = 0


@admin.register(ForecastSeries)
class ForecastSeriesAdmin(admin.ModelAdmin):
    list_display = ('module', 'metric', 'unit', 'model', 'mape', 'r_squared', 'accuracy_pct', 'horizon_days', 'created_at')
    search_fields = ('module', 'metric', 'model')
    inlines = [ForecastPointInline]


@admin.register(Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    list_display = ('module', 'metric', 'current_value', 'expected_value', 'deviation_pct', 'direction', 'severity', 'status', 'detected_at')
    search_fields = ('module', 'metric')
    list_filter = ('severity', 'status', 'direction')


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'category', 'impact', 'impact_value_aed', 'confidence_pct', 'status', 'created_at')
    search_fields = ('title', 'module')
    list_filter = ('category', 'impact', 'status')


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'created_by', 'created_at')
    search_fields = ('code', 'name')


class AIMessageInline(admin.TabularInline):
    model = AIMessage
    extra = 0


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'last_message', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [AIMessageInline]


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = ('module', 'entity', 'format', 'status', 'row_count', 'file_size_kb', 'created_by', 'completed_at', 'created_at')
    search_fields = ('module', 'entity')
    list_filter = ('format', 'status')
