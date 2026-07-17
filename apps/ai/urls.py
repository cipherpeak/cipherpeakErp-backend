from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'kpis', views.KPIViewSet, basename='kpi')
router.register(r'dashboards', views.DashboardViewSet, basename='dashboard')
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'saved-reports', views.SavedReportViewSet, basename='saved-report')
router.register(r'scheduled-reports', views.ScheduledReportViewSet, basename='scheduled-report')
router.register(r'forecasts', views.ForecastSeriesViewSet, basename='forecast')
router.register(r'anomalies', views.AnomalyViewSet, basename='anomaly')
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')
router.register(r'scenarios', views.ScenarioViewSet, basename='scenario')
router.register(r'conversations', views.AIConversationViewSet, basename='ai-conversation')
router.register(r'export-jobs', views.ExportJobViewSet, basename='export-job')

urlpatterns = [
    path('', include(router.urls)),
]
