from typing import Dict, Any, List
from .models import (
    KPI, KPIHistory, KPIAlert, Dashboard, DashboardWidget, Report, SavedReport,
    ScheduledReport, ForecastSeries, ForecastPoint, Anomaly, Recommendation,
    Scenario, AIConversation, AIMessage, ExportJob,
)


# ===========================================================================
# KPI SERVICES
# ===========================================================================

def get_all_kpis() -> List[KPI]:
    return KPI.objects.filter(is_deleted=False)

def get_kpi_with_details(kpi_id: int) -> KPI:
    return KPI.objects.prefetch_related('history', 'alerts').get(pk=kpi_id)

def create_kpi(data: Dict[str, Any]) -> KPI:
    history_data = data.pop('history', [])
    alerts_data = data.pop('alerts', [])
    kpi = KPI.objects.create(**data)
    for h_data in history_data:
        KPIHistory.objects.create(kpi=kpi, **h_data)
    for a_data in alerts_data:
        KPIAlert.objects.create(kpi=kpi, **a_data)
    return kpi

def update_kpi(kpi: KPI, data: Dict[str, Any]) -> KPI:
    data.pop('history', None)
    data.pop('alerts', None)
    for field, value in data.items():
        setattr(kpi, field, value)
    kpi.save()
    return kpi

def delete_kpi(kpi: KPI) -> None:
    kpi.is_deleted = True
    kpi.save()


# ===========================================================================
# DASHBOARD SERVICES
# ===========================================================================

def get_all_dashboards() -> List[Dashboard]:
    return Dashboard.objects.filter(is_deleted=False)

def get_dashboard_with_widgets(dashboard_id: int) -> Dashboard:
    return Dashboard.objects.prefetch_related('widgets').get(pk=dashboard_id)

def create_dashboard(data: Dict[str, Any]) -> Dashboard:
    widgets_data = data.pop('widgets', [])
    dashboard = Dashboard.objects.create(**data)
    for w_data in widgets_data:
        DashboardWidget.objects.create(dashboard=dashboard, **w_data)
    return dashboard

def update_dashboard(dashboard: Dashboard, data: Dict[str, Any]) -> Dashboard:
    data.pop('widgets', None)
    for field, value in data.items():
        setattr(dashboard, field, value)
    dashboard.save()
    return dashboard

def delete_dashboard(dashboard: Dashboard) -> None:
    dashboard.is_deleted = True
    dashboard.save()


# ===========================================================================
# REPORT SERVICES
# ===========================================================================

def get_all_reports() -> List[Report]:
    return Report.objects.filter(is_deleted=False)

def create_report(data: Dict[str, Any]) -> Report:
    return Report.objects.create(**data)

def update_report(report: Report, data: Dict[str, Any]) -> Report:
    for field, value in data.items():
        setattr(report, field, value)
    report.save()
    return report

def delete_report(report: Report) -> None:
    report.is_deleted = True
    report.save()


# ===========================================================================
# SAVED REPORT SERVICES
# ===========================================================================

def get_all_saved_reports() -> List[SavedReport]:
    return SavedReport.objects.all()

def create_saved_report(data: Dict[str, Any]) -> SavedReport:
    return SavedReport.objects.create(**data)

def update_saved_report(saved: SavedReport, data: Dict[str, Any]) -> SavedReport:
    for field, value in data.items():
        setattr(saved, field, value)
    saved.save()
    return saved

def delete_saved_report(saved: SavedReport) -> None:
    saved.delete()


# ===========================================================================
# SCHEDULED REPORT SERVICES
# ===========================================================================

def get_all_scheduled_reports() -> List[ScheduledReport]:
    return ScheduledReport.objects.filter(is_deleted=False)

def create_scheduled_report(data: Dict[str, Any]) -> ScheduledReport:
    return ScheduledReport.objects.create(**data)

def update_scheduled_report(schedule: ScheduledReport, data: Dict[str, Any]) -> ScheduledReport:
    for field, value in data.items():
        setattr(schedule, field, value)
    schedule.save()
    return schedule

def delete_scheduled_report(schedule: ScheduledReport) -> None:
    schedule.is_deleted = True
    schedule.save()


# ===========================================================================
# FORECAST SERVICES
# ===========================================================================

def get_all_forecast_series() -> List[ForecastSeries]:
    return ForecastSeries.objects.all()

def get_forecast_with_points(series_id: int) -> ForecastSeries:
    return ForecastSeries.objects.prefetch_related('points').get(pk=series_id)

def create_forecast_series(data: Dict[str, Any]) -> ForecastSeries:
    points_data = data.pop('points', [])
    series = ForecastSeries.objects.create(**data)
    for p_data in points_data:
        ForecastPoint.objects.create(series=series, **p_data)
    return series

def update_forecast_series(series: ForecastSeries, data: Dict[str, Any]) -> ForecastSeries:
    data.pop('points', None)
    for field, value in data.items():
        setattr(series, field, value)
    series.save()
    return series

def delete_forecast_series(series: ForecastSeries) -> None:
    series.delete()


# ===========================================================================
# ANOMALY SERVICES
# ===========================================================================

def get_all_anomalies() -> List[Anomaly]:
    return Anomaly.objects.filter(is_deleted=False)

def create_anomaly(data: Dict[str, Any]) -> Anomaly:
    return Anomaly.objects.create(**data)

def update_anomaly(anomaly: Anomaly, data: Dict[str, Any]) -> Anomaly:
    for field, value in data.items():
        setattr(anomaly, field, value)
    anomaly.save()
    return anomaly

def delete_anomaly(anomaly: Anomaly) -> None:
    anomaly.is_deleted = True
    anomaly.save()


# ===========================================================================
# RECOMMENDATION SERVICES
# ===========================================================================

def get_all_recommendations() -> List[Recommendation]:
    return Recommendation.objects.filter(is_deleted=False)

def create_recommendation(data: Dict[str, Any]) -> Recommendation:
    return Recommendation.objects.create(**data)

def update_recommendation(recommendation: Recommendation, data: Dict[str, Any]) -> Recommendation:
    for field, value in data.items():
        setattr(recommendation, field, value)
    recommendation.save()
    return recommendation

def delete_recommendation(recommendation: Recommendation) -> None:
    recommendation.is_deleted = True
    recommendation.save()


# ===========================================================================
# SCENARIO SERVICES
# ===========================================================================

def get_all_scenarios() -> List[Scenario]:
    return Scenario.objects.filter(is_deleted=False)

def create_scenario(data: Dict[str, Any]) -> Scenario:
    return Scenario.objects.create(**data)

def update_scenario(scenario: Scenario, data: Dict[str, Any]) -> Scenario:
    for field, value in data.items():
        setattr(scenario, field, value)
    scenario.save()
    return scenario

def delete_scenario(scenario: Scenario) -> None:
    scenario.is_deleted = True
    scenario.save()


# ===========================================================================
# AI CONVERSATION SERVICES
# ===========================================================================

def get_all_conversations() -> List[AIConversation]:
    return AIConversation.objects.all()

def get_conversation_with_messages(conversation_id: int) -> AIConversation:
    return AIConversation.objects.prefetch_related('messages').get(pk=conversation_id)

def create_conversation(data: Dict[str, Any]) -> AIConversation:
    messages_data = data.pop('messages', [])
    conversation = AIConversation.objects.create(**data)
    for m_data in messages_data:
        AIMessage.objects.create(conversation=conversation, **m_data)
    return conversation

def update_conversation(conversation: AIConversation, data: Dict[str, Any]) -> AIConversation:
    data.pop('messages', None)
    for field, value in data.items():
        setattr(conversation, field, value)
    conversation.save()
    return conversation

def delete_conversation(conversation: AIConversation) -> None:
    conversation.delete()

def add_message(conversation: AIConversation, data: Dict[str, Any]) -> AIMessage:
    message = AIMessage.objects.create(conversation=conversation, **data)
    conversation.last_message = data.get('content', conversation.last_message)
    conversation.save()
    return message


# ===========================================================================
# EXPORT JOB SERVICES
# ===========================================================================

def get_all_export_jobs() -> List[ExportJob]:
    return ExportJob.objects.all()

def create_export_job(data: Dict[str, Any]) -> ExportJob:
    return ExportJob.objects.create(**data)

def update_export_job(job: ExportJob, data: Dict[str, Any]) -> ExportJob:
    for field, value in data.items():
        setattr(job, field, value)
    job.save()
    return job

def delete_export_job(job: ExportJob) -> None:
    job.delete()
