from django.contrib import admin
from .models import (
    CalendarEvent, Event, EventAttendee, EventReminder, EventActivity,
    Meeting, MeetingAttendee, MeetingAgendaItem, Holiday, Reminder,
    CalendarResource, ResourceBooking, SharedCalendar, CalendarSubscription,
    CalendarNotification,
)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'date_start', 'date_end', 'all_day', 'location', 'attendee_count', 'created_at')
    search_fields = ('title', 'location')
    list_filter = ('category', 'status', 'recurrence')


class EventAttendeeInline(admin.TabularInline):
    model = EventAttendee
    extra = 0


class EventReminderInline(admin.TabularInline):
    model = EventReminder
    extra = 0


class EventActivityInline(admin.TabularInline):
    model = EventActivity
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'type', 'status', 'category', 'date_start', 'date_end', 'organiser', 'created_at')
    search_fields = ('code', 'title', 'organiser')
    list_filter = ('type', 'status', 'category')
    inlines = [EventAttendeeInline, EventReminderInline, EventActivityInline]


class MeetingAttendeeInline(admin.TabularInline):
    model = MeetingAttendee
    extra = 0


class MeetingAgendaItemInline(admin.TabularInline):
    model = MeetingAgendaItem
    extra = 0


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'type', 'status', 'meeting_date', 'time_start', 'time_end', 'organiser', 'location', 'created_at')
    search_fields = ('code', 'title', 'organiser')
    list_filter = ('type', 'status')
    inlines = [MeetingAttendeeInline, MeetingAgendaItemInline]


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'holiday_date', 'date_end', 'type', 'applicable_to', 'is_optional', 'created_at')
    search_fields = ('name',)
    list_filter = ('type', 'is_optional')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'due_time', 'type', 'status', 'repeat', 'owner', 'created_at')
    search_fields = ('title',)
    list_filter = ('status', 'type', 'repeat')


class ResourceBookingInline(admin.TabularInline):
    model = ResourceBooking
    extra = 0


@admin.register(CalendarResource)
class CalendarResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'capacity', 'status', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('status', 'type')
    inlines = [ResourceBookingInline]


class CalendarSubscriptionInline(admin.TabularInline):
    model = CalendarSubscription
    extra = 0


@admin.register(SharedCalendar)
class SharedCalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'owner', 'owner_dept', 'status', 'subscriber_count', 'is_default', 'created_at')
    search_fields = ('name', 'owner')
    list_filter = ('type', 'status', 'is_default')
    inlines = [CalendarSubscriptionInline]


@admin.register(CalendarNotification)
class CalendarNotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'from_user', 'recipient', 'event_title', 'event_date', 'status', 'action_required', 'created_at')
    search_fields = ('title', 'from_user', 'event_title')
    list_filter = ('type', 'status', 'action_required')
