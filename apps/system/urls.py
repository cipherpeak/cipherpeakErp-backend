from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'users', views.SystemUserViewSet, basename='systemuser')
router.register(r'workflows', views.ApprovalWorkflowViewSet, basename='workflow')
router.register(r'delegations', views.DelegationViewSet, basename='delegation')
router.register(r'login-events', views.LoginEventViewSet, basename='login-event')
router.register(r'device-sessions', views.DeviceSessionViewSet, basename='device-session')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
