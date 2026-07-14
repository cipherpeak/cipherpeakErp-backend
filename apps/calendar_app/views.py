from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    CalendarEvent, Event, Meeting, Holiday, Reminder,
    CalendarResource, SharedCalendar, CalendarNotification,
)
from .serializers import (
    CalendarEventSerializer, EventSerializer, MeetingSerializer, HolidaySerializer,
    ReminderSerializer, CalendarResourceSerializer, SharedCalendarSerializer,
    CalendarNotificationSerializer,
)
from . import services


# ===========================================================================
# CALENDAR EVENT VIEWSET
# ===========================================================================

class CalendarEventViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(CalendarEventSerializer(services.get_all_calendar_events(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(CalendarEventSerializer(get_object_or_404(CalendarEvent, pk=pk)).data)

    def create(self, request):
        serializer = CalendarEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_calendar_event(serializer.validated_data)
        return Response({"message": "Calendar event created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        event = get_object_or_404(CalendarEvent, pk=pk)
        serializer = CalendarEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_calendar_event(event, serializer.validated_data)
        return Response({"message": "Calendar event updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        event = get_object_or_404(CalendarEvent, pk=pk)
        serializer = CalendarEventSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_calendar_event(event, serializer.validated_data)
        return Response({"message": "Calendar event updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_calendar_event(get_object_or_404(CalendarEvent, pk=pk))
        return Response({"message": "Calendar event deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# EVENT VIEWSET
# ===========================================================================

class EventViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(EventSerializer(services.get_all_events(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(EventSerializer(services.get_event_with_details(pk)).data)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_event(serializer.validated_data)
            return Response({"message": "Event created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_event(event, serializer.validated_data)
            return Response({"message": "Event updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_event(event, serializer.validated_data)
            return Response({"message": "Event updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_event(get_object_or_404(Event, pk=pk))
        return Response({"message": "Event deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# MEETING VIEWSET
# ===========================================================================

class MeetingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(MeetingSerializer(services.get_all_meetings(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(MeetingSerializer(services.get_meeting_with_details(pk)).data)

    def create(self, request):
        serializer = MeetingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_meeting(serializer.validated_data)
            return Response({"message": "Meeting created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        meeting = get_object_or_404(Meeting, pk=pk)
        serializer = MeetingSerializer(meeting, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_meeting(meeting, serializer.validated_data)
            return Response({"message": "Meeting updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        meeting = get_object_or_404(Meeting, pk=pk)
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_meeting(meeting, serializer.validated_data)
            return Response({"message": "Meeting updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_meeting(get_object_or_404(Meeting, pk=pk))
        return Response({"message": "Meeting deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# HOLIDAY VIEWSET
# ===========================================================================

class HolidayViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(HolidaySerializer(services.get_all_holidays(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(HolidaySerializer(get_object_or_404(Holiday, pk=pk)).data)

    def create(self, request):
        serializer = HolidaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_holiday(serializer.validated_data)
        return Response({"message": "Holiday created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        holiday = get_object_or_404(Holiday, pk=pk)
        serializer = HolidaySerializer(holiday, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_holiday(holiday, serializer.validated_data)
        return Response({"message": "Holiday updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        holiday = get_object_or_404(Holiday, pk=pk)
        serializer = HolidaySerializer(holiday, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_holiday(holiday, serializer.validated_data)
        return Response({"message": "Holiday updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_holiday(get_object_or_404(Holiday, pk=pk))
        return Response({"message": "Holiday deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# REMINDER VIEWSET
# ===========================================================================

class ReminderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ReminderSerializer(services.get_all_reminders(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ReminderSerializer(get_object_or_404(Reminder, pk=pk)).data)

    def create(self, request):
        serializer = ReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_reminder(serializer.validated_data)
        return Response({"message": "Reminder created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        reminder = get_object_or_404(Reminder, pk=pk)
        serializer = ReminderSerializer(reminder, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_reminder(reminder, serializer.validated_data)
        return Response({"message": "Reminder updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        reminder = get_object_or_404(Reminder, pk=pk)
        serializer = ReminderSerializer(reminder, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_reminder(reminder, serializer.validated_data)
        return Response({"message": "Reminder updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_reminder(get_object_or_404(Reminder, pk=pk))
        return Response({"message": "Reminder deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CALENDAR RESOURCE VIEWSET
# ===========================================================================

class CalendarResourceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(CalendarResourceSerializer(services.get_all_resources(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(CalendarResourceSerializer(services.get_resource_with_bookings(pk)).data)

    def create(self, request):
        serializer = CalendarResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_resource(serializer.validated_data)
        return Response({"message": "Calendar resource created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        resource = get_object_or_404(CalendarResource, pk=pk)
        serializer = CalendarResourceSerializer(resource, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_resource(resource, serializer.validated_data)
        return Response({"message": "Calendar resource updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        resource = get_object_or_404(CalendarResource, pk=pk)
        serializer = CalendarResourceSerializer(resource, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_resource(resource, serializer.validated_data)
        return Response({"message": "Calendar resource updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_resource(get_object_or_404(CalendarResource, pk=pk))
        return Response({"message": "Calendar resource deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SHARED CALENDAR VIEWSET
# ===========================================================================

class SharedCalendarViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(SharedCalendarSerializer(services.get_all_shared_calendars(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(SharedCalendarSerializer(services.get_shared_calendar_with_subscriptions(pk)).data)

    def create(self, request):
        serializer = SharedCalendarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_shared_calendar(serializer.validated_data)
        return Response({"message": "Shared calendar created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        calendar = get_object_or_404(SharedCalendar, pk=pk)
        serializer = SharedCalendarSerializer(calendar, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_shared_calendar(calendar, serializer.validated_data)
        return Response({"message": "Shared calendar updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        calendar = get_object_or_404(SharedCalendar, pk=pk)
        serializer = SharedCalendarSerializer(calendar, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_shared_calendar(calendar, serializer.validated_data)
        return Response({"message": "Shared calendar updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_shared_calendar(get_object_or_404(SharedCalendar, pk=pk))
        return Response({"message": "Shared calendar deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CALENDAR NOTIFICATION VIEWSET
# ===========================================================================

class CalendarNotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(CalendarNotificationSerializer(services.get_all_notifications(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(CalendarNotificationSerializer(get_object_or_404(CalendarNotification, pk=pk)).data)

    def create(self, request):
        serializer = CalendarNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_notification(serializer.validated_data)
        return Response({"message": "Calendar notification created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        notification = get_object_or_404(CalendarNotification, pk=pk)
        serializer = CalendarNotificationSerializer(notification, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_notification(notification, serializer.validated_data)
        return Response({"message": "Calendar notification updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        notification = get_object_or_404(CalendarNotification, pk=pk)
        serializer = CalendarNotificationSerializer(notification, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_notification(notification, serializer.validated_data)
        return Response({"message": "Calendar notification updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_notification(get_object_or_404(CalendarNotification, pk=pk))
        return Response({"message": "Calendar notification deleted successfully."}, status=status.HTTP_200_OK)
