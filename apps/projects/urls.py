from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'milestones', views.MilestoneViewSet, basename='milestone')
router.register(r'tasks', views.ProjectTaskViewSet, basename='project-task')
router.register(r'sites', views.SiteViewSet, basename='site')
router.register(r'resources', views.ResourceViewSet, basename='resource')
router.register(r'timesheets', views.TimesheetViewSet, basename='timesheet')
router.register(r'billings', views.ProjectBillingViewSet, basename='project-billing')
router.register(r'costings', views.ProjectCostingViewSet, basename='project-costing')

urlpatterns = [
    path('', include(router.urls)),
]
