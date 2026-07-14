from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'quality-checks', views.QualityCheckViewSet, basename='quality-check')
router.register(r'defect-categories', views.DefectCategoryViewSet, basename='defect-category')
router.register(r'inspections', views.InspectionViewSet, basename='inspection')
router.register(r'ncr-records', views.NCRRecordViewSet, basename='ncr-record')
router.register(r'capa-records', views.CAPARecordViewSet, basename='capa-record')
router.register(r'rework-records', views.ReworkRecordViewSet, basename='rework-record')

urlpatterns = [
    path('', include(router.urls)),
]
