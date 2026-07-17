from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    KPI, Dashboard, Report, SavedReport, ScheduledReport, ForecastSeries,
    Anomaly, Recommendation, Scenario, AIConversation, ExportJob,
)
from .serializers import (
    KPISerializer, DashboardSerializer, ReportSerializer, SavedReportSerializer,
    ScheduledReportSerializer, ForecastSeriesSerializer, AnomalySerializer,
    RecommendationSerializer, ScenarioSerializer, AIConversationSerializer,
    AIMessageSerializer, ExportJobSerializer,
)
from . import services


# ===========================================================================
# KPI VIEWSET
# ===========================================================================

class KPIViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(KPISerializer(services.get_all_kpis(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(KPISerializer(services.get_kpi_with_details(pk)).data)

    def create(self, request):
        serializer = KPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_kpi(serializer.validated_data)
        return Response({"message": "KPI created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        kpi = get_object_or_404(KPI, pk=pk)
        serializer = KPISerializer(kpi, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_kpi(kpi, serializer.validated_data)
        return Response({"message": "KPI updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        kpi = get_object_or_404(KPI, pk=pk)
        serializer = KPISerializer(kpi, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_kpi(kpi, serializer.validated_data)
        return Response({"message": "KPI updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_kpi(get_object_or_404(KPI, pk=pk))
        return Response({"message": "KPI deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# DASHBOARD VIEWSET
# ===========================================================================

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(DashboardSerializer(services.get_all_dashboards(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(DashboardSerializer(services.get_dashboard_with_widgets(pk)).data)

    def create(self, request):
        serializer = DashboardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_dashboard(serializer.validated_data)
        return Response({"message": "Dashboard created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        dashboard = get_object_or_404(Dashboard, pk=pk)
        serializer = DashboardSerializer(dashboard, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_dashboard(dashboard, serializer.validated_data)
        return Response({"message": "Dashboard updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        dashboard = get_object_or_404(Dashboard, pk=pk)
        serializer = DashboardSerializer(dashboard, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_dashboard(dashboard, serializer.validated_data)
        return Response({"message": "Dashboard updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_dashboard(get_object_or_404(Dashboard, pk=pk))
        return Response({"message": "Dashboard deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# REPORT VIEWSET
# ===========================================================================

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ReportSerializer(services.get_all_reports(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ReportSerializer(get_object_or_404(Report, pk=pk)).data)

    def create(self, request):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_report(serializer.validated_data)
        return Response({"message": "Report created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        report = get_object_or_404(Report, pk=pk)
        serializer = ReportSerializer(report, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_report(report, serializer.validated_data)
        return Response({"message": "Report updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        report = get_object_or_404(Report, pk=pk)
        serializer = ReportSerializer(report, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_report(report, serializer.validated_data)
        return Response({"message": "Report updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_report(get_object_or_404(Report, pk=pk))
        return Response({"message": "Report deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SAVED REPORT VIEWSET
# ===========================================================================

class SavedReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(SavedReportSerializer(services.get_all_saved_reports(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(SavedReportSerializer(get_object_or_404(SavedReport, pk=pk)).data)

    def create(self, request):
        serializer = SavedReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_saved_report(serializer.validated_data)
        return Response({"message": "Saved report created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        saved = get_object_or_404(SavedReport, pk=pk)
        serializer = SavedReportSerializer(saved, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_saved_report(saved, serializer.validated_data)
        return Response({"message": "Saved report updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        saved = get_object_or_404(SavedReport, pk=pk)
        serializer = SavedReportSerializer(saved, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_saved_report(saved, serializer.validated_data)
        return Response({"message": "Saved report updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_saved_report(get_object_or_404(SavedReport, pk=pk))
        return Response({"message": "Saved report deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SCHEDULED REPORT VIEWSET
# ===========================================================================

class ScheduledReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ScheduledReportSerializer(services.get_all_scheduled_reports(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ScheduledReportSerializer(get_object_or_404(ScheduledReport, pk=pk)).data)

    def create(self, request):
        serializer = ScheduledReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_scheduled_report(serializer.validated_data)
        return Response({"message": "Scheduled report created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        schedule = get_object_or_404(ScheduledReport, pk=pk)
        serializer = ScheduledReportSerializer(schedule, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_scheduled_report(schedule, serializer.validated_data)
        return Response({"message": "Scheduled report updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        schedule = get_object_or_404(ScheduledReport, pk=pk)
        serializer = ScheduledReportSerializer(schedule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_scheduled_report(schedule, serializer.validated_data)
        return Response({"message": "Scheduled report updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_scheduled_report(get_object_or_404(ScheduledReport, pk=pk))
        return Response({"message": "Scheduled report deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# FORECAST SERIES VIEWSET
# ===========================================================================

class ForecastSeriesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ForecastSeriesSerializer(services.get_all_forecast_series(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ForecastSeriesSerializer(services.get_forecast_with_points(pk)).data)

    def create(self, request):
        serializer = ForecastSeriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_forecast_series(serializer.validated_data)
        return Response({"message": "Forecast series created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        series = get_object_or_404(ForecastSeries, pk=pk)
        serializer = ForecastSeriesSerializer(series, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_forecast_series(series, serializer.validated_data)
        return Response({"message": "Forecast series updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        series = get_object_or_404(ForecastSeries, pk=pk)
        serializer = ForecastSeriesSerializer(series, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_forecast_series(series, serializer.validated_data)
        return Response({"message": "Forecast series updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_forecast_series(get_object_or_404(ForecastSeries, pk=pk))
        return Response({"message": "Forecast series deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# ANOMALY VIEWSET
# ===========================================================================

class AnomalyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(AnomalySerializer(services.get_all_anomalies(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(AnomalySerializer(get_object_or_404(Anomaly, pk=pk)).data)

    def create(self, request):
        serializer = AnomalySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_anomaly(serializer.validated_data)
        return Response({"message": "Anomaly created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        anomaly = get_object_or_404(Anomaly, pk=pk)
        serializer = AnomalySerializer(anomaly, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_anomaly(anomaly, serializer.validated_data)
        return Response({"message": "Anomaly updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        anomaly = get_object_or_404(Anomaly, pk=pk)
        serializer = AnomalySerializer(anomaly, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_anomaly(anomaly, serializer.validated_data)
        return Response({"message": "Anomaly updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_anomaly(get_object_or_404(Anomaly, pk=pk))
        return Response({"message": "Anomaly deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# RECOMMENDATION VIEWSET
# ===========================================================================

class RecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(RecommendationSerializer(services.get_all_recommendations(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(RecommendationSerializer(get_object_or_404(Recommendation, pk=pk)).data)

    def create(self, request):
        serializer = RecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_recommendation(serializer.validated_data)
        return Response({"message": "Recommendation created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        recommendation = get_object_or_404(Recommendation, pk=pk)
        serializer = RecommendationSerializer(recommendation, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_recommendation(recommendation, serializer.validated_data)
        return Response({"message": "Recommendation updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        recommendation = get_object_or_404(Recommendation, pk=pk)
        serializer = RecommendationSerializer(recommendation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_recommendation(recommendation, serializer.validated_data)
        return Response({"message": "Recommendation updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_recommendation(get_object_or_404(Recommendation, pk=pk))
        return Response({"message": "Recommendation deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SCENARIO VIEWSET
# ===========================================================================

class ScenarioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ScenarioSerializer(services.get_all_scenarios(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ScenarioSerializer(get_object_or_404(Scenario, pk=pk)).data)

    def create(self, request):
        serializer = ScenarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_scenario(serializer.validated_data)
        return Response({"message": "Scenario created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        scenario = get_object_or_404(Scenario, pk=pk)
        serializer = ScenarioSerializer(scenario, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_scenario(scenario, serializer.validated_data)
        return Response({"message": "Scenario updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        scenario = get_object_or_404(Scenario, pk=pk)
        serializer = ScenarioSerializer(scenario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_scenario(scenario, serializer.validated_data)
        return Response({"message": "Scenario updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_scenario(get_object_or_404(Scenario, pk=pk))
        return Response({"message": "Scenario deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# AI CONVERSATION VIEWSET
# ===========================================================================

class AIConversationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(AIConversationSerializer(services.get_all_conversations(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(AIConversationSerializer(services.get_conversation_with_messages(pk)).data)

    def create(self, request):
        serializer = AIConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_conversation(serializer.validated_data)
        return Response({"message": "Conversation created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        conversation = get_object_or_404(AIConversation, pk=pk)
        serializer = AIConversationSerializer(conversation, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_conversation(conversation, serializer.validated_data)
        return Response({"message": "Conversation updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        conversation = get_object_or_404(AIConversation, pk=pk)
        serializer = AIConversationSerializer(conversation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_conversation(conversation, serializer.validated_data)
        return Response({"message": "Conversation updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_conversation(get_object_or_404(AIConversation, pk=pk))
        return Response({"message": "Conversation deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='messages')
    def add_message(self, request, pk=None):
        conversation = get_object_or_404(AIConversation, pk=pk)
        serializer = AIMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.add_message(conversation, serializer.validated_data)
        return Response({"message": "Message added successfully."}, status=status.HTTP_201_CREATED)


# ===========================================================================
# EXPORT JOB VIEWSET
# ===========================================================================

class ExportJobViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ExportJobSerializer(services.get_all_export_jobs(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ExportJobSerializer(get_object_or_404(ExportJob, pk=pk)).data)

    def create(self, request):
        serializer = ExportJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_export_job(serializer.validated_data)
        return Response({"message": "Export job created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        job = get_object_or_404(ExportJob, pk=pk)
        serializer = ExportJobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_export_job(job, serializer.validated_data)
        return Response({"message": "Export job updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        job = get_object_or_404(ExportJob, pk=pk)
        serializer = ExportJobSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_export_job(job, serializer.validated_data)
        return Response({"message": "Export job updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_export_job(get_object_or_404(ExportJob, pk=pk))
        return Response({"message": "Export job deleted successfully."}, status=status.HTTP_200_OK)
