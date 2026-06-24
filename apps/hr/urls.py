from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'attendance', views.AttendanceRecordViewSet, basename='attendance')
router.register(r'leave-requests', views.LeaveRequestViewSet, basename='leave-request')
router.register(r'documents', views.EmpDocumentViewSet, basename='document')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login/', views.EmployeeLoginView.as_view(), name='employee-login'),
    path('', include(router.urls)),
]
