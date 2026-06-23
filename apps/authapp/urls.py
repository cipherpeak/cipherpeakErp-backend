from django.urls import path
from .views import EmployeeLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
