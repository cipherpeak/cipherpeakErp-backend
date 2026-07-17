from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class KPIStatus(models.TextChoices):
    ON_TRACK = 'on_track', 'On Track'
    AT_RISK = 'at_risk', 'At Risk'
    OFF_TRACK = 'off_track', 'Off Track'


class KPITrend(models.TextChoices):
    UP = 'up', 'Up'
    DOWN = 'down', 'Down'
    FLAT = 'flat', 'Flat'


class KPIFrequency(models.TextChoices):
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'


class ReportStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class ScheduleFrequency(models.TextChoices):
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'


class ExportFormat(models.TextChoices):
    PDF = 'pdf', 'PDF'
    EXCEL = 'excel', 'Excel'
    CSV = 'csv', 'CSV'
    JSON = 'json', 'JSON'


class ExportStatus(models.TextChoices):
    QUEUED = 'queued', 'Queued'
    PROCESSING = 'processing', 'Processing'
    COMPLETE = 'complete', 'Complete'
    FAILED = 'failed', 'Failed'


class AnomalySeverity(models.TextChoices):
    CRITICAL = 'critical', 'Critical'
    HIGH = 'high', 'High'
    MEDIUM = 'medium', 'Medium'
    LOW = 'low', 'Low'


class AnomalyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INVESTIGATING = 'investigating', 'Investigating'
    RESOLVED = 'resolved', 'Resolved'
    DISMISSED = 'dismissed', 'Dismissed'


class RecommendationStatus(models.TextChoices):
    NEW = 'new', 'New'
    ACCEPTED = 'accepted', 'Accepted'
    DISMISSED = 'dismissed', 'Dismissed'
    IMPLEMENTED = 'implemented', 'Implemented'


# ---------------------------------------------------------------------------
# KPI
# ---------------------------------------------------------------------------

class KPI(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    formula = models.TextField(blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    owner = models.CharField(max_length=150, blank=True, null=True)
    unit = models.CharField(max_length=40, blank=True, null=True)
    value = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    target = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    change_pct = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    trend = models.CharField(max_length=10, choices=KPITrend.choices, blank=True, null=True)
    status = models.CharField(max_length=20, choices=KPIStatus.choices, default=KPIStatus.ON_TRACK)
    frequency = models.CharField(max_length=20, choices=KPIFrequency.choices, blank=True, null=True)
    contributing_factors = models.JSONField(default=list, blank=True)
    linked_reports = models.JSONField(default=list, blank=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
        ordering = ['name']

    def __str__(self):
        return self.name


class KPIHistory(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='history')
    point_date = models.DateField()
    value = models.DecimalField(max_digits=18, decimal_places=4)

    class Meta:
        verbose_name = 'KPI History'
        verbose_name_plural = 'KPI History'
        ordering = ['point_date']

    def __str__(self):
        return f"{self.kpi.name} - {self.point_date}"


class KPIAlert(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='alerts')
    threshold = models.DecimalField(max_digits=18, decimal_places=4)
    condition = models.CharField(max_length=10, blank=True, null=True, help_text='above/below')
    severity = models.CharField(max_length=10, blank=True, null=True, help_text='info/warning/critical')
    recipients = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = 'KPI Alert'
        verbose_name_plural = 'KPI Alerts'

    def __str__(self):
        return f"{self.kpi.name} - {self.condition} {self.threshold}"


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='dashboards',
    )
    last_viewed = models.DateTimeField(blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['name']

    def __str__(self):
        return self.name


class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    type = models.CharField(max_length=20, help_text='stat/bar/line/donut/table/gauge/funnel/area')
    title = models.CharField(max_length=200, blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    data_key = models.CharField(max_length=120, blank=True, null=True)
    col_span = models.SmallIntegerField(default=1)
    row_span = models.SmallIntegerField(default=1)
    color = models.CharField(max_length=40, blank=True, null=True)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'

    def __str__(self):
        return f"{self.dashboard.name} - {self.title}"


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

class Report(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ReportStatus.choices, default=ReportStatus.DRAFT)
    chart_type = models.CharField(max_length=20, default='none')
    columns = models.JSONField(default=list, blank=True)
    filters = models.JSONField(default=list, blank=True)
    sort = models.JSONField(default=dict, blank=True)
    group_by = models.CharField(max_length=120, blank=True, null=True)
    row_count = models.IntegerField(default=0)
    is_scheduled = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='reports',
    )
    last_run = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Saved Report (snapshot)
# ---------------------------------------------------------------------------

class SavedReport(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.SET_NULL, blank=True, null=True, related_name='snapshots',
    )
    report_name = models.CharField(max_length=200, blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    snapshot_date = models.DateTimeField(blank=True, null=True)
    row_count = models.IntegerField(blank=True, null=True)
    file_size_kb = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, choices=ExportFormat.choices, blank=True, null=True)
    generated_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='generated_reports',
    )
    expires_at = models.DateTimeField(blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = 'Saved Report'
        verbose_name_plural = 'Saved Reports'
        ordering = ['-snapshot_date']

    def __str__(self):
        return self.report_name or f"Snapshot {self.id}"


# ---------------------------------------------------------------------------
# Scheduled Report
# ---------------------------------------------------------------------------

class ScheduledReport(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='schedules')
    report_name = models.CharField(max_length=200, blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    frequency = models.CharField(max_length=20, choices=ScheduleFrequency.choices)
    day_of_week = models.CharField(max_length=12, blank=True, null=True)
    day_of_month = models.SmallIntegerField(blank=True, null=True)
    run_time = models.TimeField(blank=True, null=True)
    recipients = models.JSONField(default=list, blank=True)
    format = models.CharField(max_length=10, choices=ExportFormat.choices, blank=True, null=True)
    last_run = models.DateTimeField(blank=True, null=True)
    last_run_status = models.CharField(max_length=12, blank=True, null=True, help_text='success/failed/skipped')
    next_run = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, default='active', help_text='active/paused/failed')
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='scheduled_reports',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Scheduled Report'
        verbose_name_plural = 'Scheduled Reports'
        ordering = ['-created_at']

    def __str__(self):
        return self.report_name or f"Schedule {self.id}"


# ---------------------------------------------------------------------------
# Forecast
# ---------------------------------------------------------------------------

class ForecastSeries(models.Model):
    module = models.CharField(max_length=40, blank=True, null=True, help_text='Revenue/Demand/Cash Flow/Headcount')
    metric = models.CharField(max_length=120, blank=True, null=True)
    unit = models.CharField(max_length=40, blank=True, null=True)
    model = models.CharField(max_length=80, blank=True, null=True)
    mape = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    r_squared = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    accuracy_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    horizon_days = models.IntegerField(blank=True, null=True)
    insights = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Forecast Series'
        verbose_name_plural = 'Forecast Series'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.module} - {self.metric}"


class ForecastPoint(models.Model):
    series = models.ForeignKey(ForecastSeries, on_delete=models.CASCADE, related_name='points')
    period = models.CharField(max_length=40)
    actual = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    forecast = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    lower_bound = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    upper_bound = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    is_forecast = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Forecast Point'
        verbose_name_plural = 'Forecast Points'

    def __str__(self):
        return f"{self.series_id} - {self.period}"


# ---------------------------------------------------------------------------
# Anomaly
# ---------------------------------------------------------------------------

class Anomaly(models.Model):
    module = models.CharField(max_length=60, blank=True, null=True)
    metric = models.CharField(max_length=120, blank=True, null=True)
    current_value = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    expected_value = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    deviation_pct = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    direction = models.CharField(max_length=10, blank=True, null=True, help_text='spike/drop/trend')
    severity = models.CharField(max_length=10, choices=AnomalySeverity.choices)
    status = models.CharField(max_length=20, choices=AnomalyStatus.choices, default=AnomalyStatus.ACTIVE)
    detected_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    possible_cause = models.TextField(blank=True, null=True)
    recommended_action = models.TextField(blank=True, null=True)
    sparkline = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Anomaly'
        verbose_name_plural = 'Anomalies'
        ordering = ['-detected_at']

    def __str__(self):
        return f"{self.module} - {self.metric}"


# ---------------------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------------------

class Recommendation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True, help_text='cost_saving/risk_alert/efficiency/revenue/compliance')
    impact = models.CharField(max_length=10, blank=True, null=True, help_text='high/medium/low')
    impact_value_aed = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    confidence_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=RecommendationStatus.choices, default=RecommendationStatus.NEW)
    action_label = models.CharField(max_length=120, blank=True, null=True)
    action_route = models.CharField(max_length=200, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Scenario
# ---------------------------------------------------------------------------

class Scenario(models.Model):
    code = models.CharField(max_length=30, help_text='base/optimistic/pessimistic/custom')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=40, blank=True, null=True)
    lever_overrides = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='scenarios',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Scenario'
        verbose_name_plural = 'Scenarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------------------------------------------------------------------
# AI Assistant
# ---------------------------------------------------------------------------

class AIConversation(models.Model):
    user = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='ai_conversations',
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    last_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'AI Conversation'
        verbose_name_plural = 'AI Conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class AIMessage(models.Model):
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=12, help_text='user/assistant')
    content = models.TextField(blank=True, null=True)
    result_type = models.CharField(max_length=12, blank=True, null=True, help_text='text/table/number/list')
    result_data = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'AI Message'
        verbose_name_plural = 'AI Messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation_id} - {self.role}"


# ---------------------------------------------------------------------------
# Export Job
# ---------------------------------------------------------------------------

class ExportJob(models.Model):
    module = models.CharField(max_length=60, blank=True, null=True)
    entity = models.CharField(max_length=120, blank=True, null=True)
    format = models.CharField(max_length=10, choices=ExportFormat.choices)
    status = models.CharField(max_length=20, choices=ExportStatus.choices, default=ExportStatus.QUEUED)
    filters = models.TextField(blank=True, null=True)
    row_count = models.IntegerField(blank=True, null=True)
    file_size_kb = models.IntegerField(blank=True, null=True)
    error_msg = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='export_jobs',
    )
    completed_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Export Job'
        verbose_name_plural = 'Export Jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.module} - {self.entity} ({self.format})"
