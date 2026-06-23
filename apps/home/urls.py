from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home-details'),
    path('checkin/', CheckInAPIView.as_view(), name='checkin'),
    path('checkout/', CheckOutAPIView.as_view(), name='checkout'),
    path('break/start/', StartBreakAPIView.as_view(), name='start-break'),
    path('break/end/', EndBreakAPIView.as_view(), name='end-break'),
    path('break/extend/', ExtendBreakAPIView.as_view(), name='extend-break'),
    path('company-announcements/', CompanyAnnouncementListAPIView.as_view(), name='company-announcements'),

    path('leave-list/', LeaveDashboardView.as_view(), name='leave-list'),
    path('leave-apply/', LeaveApplicationView.as_view(), name='leave-apply'),
    path('leave/<int:leave_id>/', LeaveDetailView.as_view(), name='leave-detail'),
    path('monthly-review/', MonthlyReviewView.as_view(), name='monthly-review'),
    path('notifications/', NotificationListAPIView.as_view(), name='api-notifications'),
    path('today/', TodayAttendanceAPIView.as_view(), name='today-attendance'),
    path('history/', AttendanceHistoryAPIView.as_view(), name='attendance-history'),

]
