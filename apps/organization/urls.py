from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'branches', views.BranchViewSet, basename='branch')
router.register(r'plants', views.PlantViewSet, basename='plant')
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'designations', views.DesignationViewSet, basename='designation')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'shifts', views.ShiftViewSet, basename='shift')
router.register(r'cost-centers', views.CostCenterViewSet, basename='cost-center')
router.register(r'org-chart', views.OrgChartViewSet, basename='org-chart')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]