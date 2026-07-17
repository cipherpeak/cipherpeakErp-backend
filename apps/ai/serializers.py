from rest_framework import serializers
from .models import (
    KPI, KPIHistory, KPIAlert, Dashboard, DashboardWidget, Report, SavedReport,
    ScheduledReport, ForecastSeries, ForecastPoint, Anomaly, Recommendation,
    Scenario, AIConversation, AIMessage, ExportJob,
)


# --- KPI + children ---

class KPIHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIHistory
        fields = '__all__'
        extra_kwargs = {'kpi': {'required': False}}


class KPIAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIAlert
        fields = '__all__'
        extra_kwargs = {'kpi': {'required': False}}


class KPISerializer(serializers.ModelSerializer):
    history = KPIHistorySerializer(many=True, required=False)
    alerts = KPIAlertSerializer(many=True, required=False)

    class Meta:
        model = KPI
        fields = '__all__'


# --- Dashboard + widgets ---

class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        extra_kwargs = {'dashboard': {'required': False}}


class DashboardSerializer(serializers.ModelSerializer):
    widgets = DashboardWidgetSerializer(many=True, required=False)

    class Meta:
        model = Dashboard
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = '__all__'


class ScheduledReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReport
        fields = '__all__'


# --- Forecast + points ---

class ForecastPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastPoint
        fields = '__all__'
        extra_kwargs = {'series': {'required': False}}


class ForecastSeriesSerializer(serializers.ModelSerializer):
    points = ForecastPointSerializer(many=True, required=False)

    class Meta:
        model = ForecastSeries
        fields = '__all__'


class AnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anomaly
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


# --- AI Conversation + messages ---

class AIMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = '__all__'
        extra_kwargs = {'conversation': {'required': False}}


class AIConversationSerializer(serializers.ModelSerializer):
    messages = AIMessageSerializer(many=True, required=False)

    class Meta:
        model = AIConversation
        fields = '__all__'


class ExportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportJob
        fields = '__all__'
