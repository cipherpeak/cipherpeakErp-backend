from typing import Dict, Any, List
from .models import (
    CalendarEvent, Event, EventAttendee, EventReminder, EventActivity,
    Meeting, MeetingAttendee, MeetingAgendaItem, Holiday, Reminder,
    CalendarResource, ResourceBooking, SharedCalendar, CalendarSubscription,
    CalendarNotification,
)


# ===========================================================================
# CALENDAR EVENT SERVICES
# ===========================================================================

def get_all_calendar_events() -> List[CalendarEvent]:
    return CalendarEvent.objects.filter(is_deleted=False)

def create_calendar_event(data: Dict[str, Any]) -> CalendarEvent:
    return CalendarEvent.objects.create(**data)

def update_calendar_event(event: CalendarEvent, data: Dict[str, Any]) -> CalendarEvent:
    for field, value in data.items():
        setattr(event, field, value)
    event.save()
    return event

def delete_calendar_event(event: CalendarEvent) -> None:
    event.is_deleted = True
    event.save()


# ===========================================================================
# EVENT SERVICES
# ===========================================================================

def get_all_events() -> List[Event]:
    return Event.objects.filter(is_deleted=False)

def get_event_with_details(event_id: int) -> Event:
    return Event.objects.prefetch_related('attendees', 'reminders', 'activities').get(pk=event_id)

def create_event(data: Dict[str, Any]) -> Event:
    code = data.get('code')
    if Event.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Event code '{code}' already exists.")
    attendees_data = data.pop('attendees', [])
    reminders_data = data.pop('reminders', [])
    activities_data = data.pop('activities', [])
    event = Event.objects.create(**data)
    for a_data in attendees_data:
        EventAttendee.objects.create(event=event, **a_data)
    for r_data in reminders_data:
        EventReminder.objects.create(event=event, **r_data)
    for act_data in activities_data:
        EventActivity.objects.create(event=event, **act_data)
    return event

def update_event(event: Event, data: Dict[str, Any]) -> Event:
    code = data.get('code')
    if code and Event.objects.filter(code__iexact=code).exclude(id=event.id).exists():
        raise ValueError(f"Event code '{code}' already exists.")
    data.pop('attendees', None)
    data.pop('reminders', None)
    data.pop('activities', None)
    for field, value in data.items():
        setattr(event, field, value)
    event.save()
    return event

def delete_event(event: Event) -> None:
    event.is_deleted = True
    event.save()


# ===========================================================================
# MEETING SERVICES
# ===========================================================================

def get_all_meetings() -> List[Meeting]:
    return Meeting.objects.filter(is_deleted=False)

def get_meeting_with_details(meeting_id: int) -> Meeting:
    return Meeting.objects.prefetch_related('attendees', 'agenda_items').get(pk=meeting_id)

def create_meeting(data: Dict[str, Any]) -> Meeting:
    code = data.get('code')
    if Meeting.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Meeting code '{code}' already exists.")
    attendees_data = data.pop('attendees', [])
    agenda_data = data.pop('agenda_items', [])
    meeting = Meeting.objects.create(**data)
    for a_data in attendees_data:
        MeetingAttendee.objects.create(meeting=meeting, **a_data)
    for ag_data in agenda_data:
        MeetingAgendaItem.objects.create(meeting=meeting, **ag_data)
    return meeting

def update_meeting(meeting: Meeting, data: Dict[str, Any]) -> Meeting:
    code = data.get('code')
    if code and Meeting.objects.filter(code__iexact=code).exclude(id=meeting.id).exists():
        raise ValueError(f"Meeting code '{code}' already exists.")
    data.pop('attendees', None)
    data.pop('agenda_items', None)
    for field, value in data.items():
        setattr(meeting, field, value)
    meeting.save()
    return meeting

def delete_meeting(meeting: Meeting) -> None:
    meeting.is_deleted = True
    meeting.save()


# ===========================================================================
# HOLIDAY SERVICES
# ===========================================================================

def get_all_holidays() -> List[Holiday]:
    return Holiday.objects.filter(is_deleted=False)

def create_holiday(data: Dict[str, Any]) -> Holiday:
    return Holiday.objects.create(**data)

def update_holiday(holiday: Holiday, data: Dict[str, Any]) -> Holiday:
    for field, value in data.items():
        setattr(holiday, field, value)
    holiday.save()
    return holiday

def delete_holiday(holiday: Holiday) -> None:
    holiday.is_deleted = True
    holiday.save()


# ===========================================================================
# REMINDER SERVICES
# ===========================================================================

def get_all_reminders() -> List[Reminder]:
    return Reminder.objects.filter(is_deleted=False)

def create_reminder(data: Dict[str, Any]) -> Reminder:
    return Reminder.objects.create(**data)

def update_reminder(reminder: Reminder, data: Dict[str, Any]) -> Reminder:
    for field, value in data.items():
        setattr(reminder, field, value)
    reminder.save()
    return reminder

def delete_reminder(reminder: Reminder) -> None:
    reminder.is_deleted = True
    reminder.save()


# ===========================================================================
# CALENDAR RESOURCE SERVICES
# ===========================================================================

def get_all_resources() -> List[CalendarResource]:
    return CalendarResource.objects.filter(is_deleted=False)

def get_resource_with_bookings(resource_id: int) -> CalendarResource:
    return CalendarResource.objects.prefetch_related('bookings').get(pk=resource_id)

def create_resource(data: Dict[str, Any]) -> CalendarResource:
    bookings_data = data.pop('bookings', [])
    resource = CalendarResource.objects.create(**data)
    for b_data in bookings_data:
        ResourceBooking.objects.create(resource=resource, **b_data)
    return resource

def update_resource(resource: CalendarResource, data: Dict[str, Any]) -> CalendarResource:
    data.pop('bookings', None)
    for field, value in data.items():
        setattr(resource, field, value)
    resource.save()
    return resource

def delete_resource(resource: CalendarResource) -> None:
    resource.is_deleted = True
    resource.save()


# ===========================================================================
# SHARED CALENDAR SERVICES
# ===========================================================================

def get_all_shared_calendars() -> List[SharedCalendar]:
    return SharedCalendar.objects.filter(is_deleted=False)

def get_shared_calendar_with_subscriptions(calendar_id: int) -> SharedCalendar:
    return SharedCalendar.objects.prefetch_related('subscriptions').get(pk=calendar_id)

def create_shared_calendar(data: Dict[str, Any]) -> SharedCalendar:
    subscriptions_data = data.pop('subscriptions', [])
    calendar = SharedCalendar.objects.create(**data)
    for s_data in subscriptions_data:
        CalendarSubscription.objects.create(shared_calendar=calendar, **s_data)
    return calendar

def update_shared_calendar(calendar: SharedCalendar, data: Dict[str, Any]) -> SharedCalendar:
    data.pop('subscriptions', None)
    for field, value in data.items():
        setattr(calendar, field, value)
    calendar.save()
    return calendar

def delete_shared_calendar(calendar: SharedCalendar) -> None:
    calendar.is_deleted = True
    calendar.save()


# ===========================================================================
# CALENDAR NOTIFICATION SERVICES
# ===========================================================================

def get_all_notifications() -> List[CalendarNotification]:
    return CalendarNotification.objects.all()

def create_notification(data: Dict[str, Any]) -> CalendarNotification:
    return CalendarNotification.objects.create(**data)

def update_notification(notification: CalendarNotification, data: Dict[str, Any]) -> CalendarNotification:
    for field, value in data.items():
        setattr(notification, field, value)
    notification.save()
    return notification

def delete_notification(notification: CalendarNotification) -> None:
    notification.delete()
