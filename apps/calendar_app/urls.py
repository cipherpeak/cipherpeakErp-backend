from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'calendar-events', views.CalendarEventViewSet, basename='calendar-event')
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'meetings', views.MeetingViewSet, basename='meeting')
router.register(r'holidays', views.HolidayViewSet, basename='holiday')
router.register(r'reminders', views.ReminderViewSet, basename='reminder')
router.register(r'resources', views.CalendarResourceViewSet, basename='calendar-resource')
router.register(r'shared-calendars', views.SharedCalendarViewSet, basename='shared-calendar')
router.register(r'notifications', views.CalendarNotificationViewSet, basename='calendar-notification')

urlpatterns = [
    path('', include(router.urls)),
]
