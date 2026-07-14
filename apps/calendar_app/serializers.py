from rest_framework import serializers
from .models import (
    CalendarEvent, Event, EventAttendee, EventReminder, EventActivity,
    Meeting, MeetingAttendee, MeetingAgendaItem, Holiday, Reminder,
    CalendarResource, ResourceBooking, SharedCalendar, CalendarSubscription,
    CalendarNotification,
)


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'


# --- Event + children ---

class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendee
        fields = '__all__'
        extra_kwargs = {'event': {'required': False}}


class EventReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventReminder
        fields = '__all__'
        extra_kwargs = {'event': {'required': False}}


class EventActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventActivity
        fields = '__all__'
        extra_kwargs = {'event': {'required': False}}


class EventSerializer(serializers.ModelSerializer):
    attendees = EventAttendeeSerializer(many=True, required=False)
    reminders = EventReminderSerializer(many=True, required=False)
    activities = EventActivitySerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'


# --- Meeting + children ---

class MeetingAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAttendee
        fields = '__all__'
        extra_kwargs = {'meeting': {'required': False}}


class MeetingAgendaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAgendaItem
        fields = '__all__'
        extra_kwargs = {'meeting': {'required': False}}


class MeetingSerializer(serializers.ModelSerializer):
    attendees = MeetingAttendeeSerializer(many=True, required=False)
    agenda_items = MeetingAgendaItemSerializer(many=True, required=False)

    class Meta:
        model = Meeting
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'


# --- Calendar Resource + bookings ---

class ResourceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceBooking
        fields = '__all__'
        extra_kwargs = {'resource': {'required': False}}


class CalendarResourceSerializer(serializers.ModelSerializer):
    bookings = ResourceBookingSerializer(many=True, required=False)

    class Meta:
        model = CalendarResource
        fields = '__all__'


# --- Shared Calendar + subscriptions ---

class CalendarSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarSubscription
        fields = '__all__'
        extra_kwargs = {'shared_calendar': {'required': False}}


class SharedCalendarSerializer(serializers.ModelSerializer):
    subscriptions = CalendarSubscriptionSerializer(many=True, required=False)

    class Meta:
        model = SharedCalendar
        fields = '__all__'


class CalendarNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarNotification
        fields = '__all__'
