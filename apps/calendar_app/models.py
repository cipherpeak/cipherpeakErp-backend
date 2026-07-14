from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CalEventCategory(models.TextChoices):
    MEETING = 'meeting', 'Meeting'
    EVENT = 'event', 'Event'
    HOLIDAY = 'holiday', 'Holiday'
    DEADLINE = 'deadline', 'Deadline'
    REMINDER = 'reminder', 'Reminder'
    BIRTHDAY = 'birthday', 'Birthday'
    OTHER = 'other', 'Other'


class CalEventStatus(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    DRAFT = 'draft', 'Draft'


class RecurrenceType(models.TextChoices):
    NONE = 'none', 'None'
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'
    YEARLY = 'yearly', 'Yearly'


class EventType(models.TextChoices):
    COMPANY_WIDE = 'company_wide', 'Company Wide'
    DEPARTMENT = 'department', 'Department'
    CLIENT = 'client', 'Client'
    TRAINING = 'training', 'Training'
    COMPLIANCE = 'compliance', 'Compliance'
    SOCIAL = 'social', 'Social'
    OTHER = 'other', 'Other'


class AttendeeStatus(models.TextChoices):
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'
    TENTATIVE = 'tentative', 'Tentative'
    PENDING = 'pending', 'Pending'


class MeetingType(models.TextChoices):
    INTERNAL = 'internal', 'Internal'
    EXTERNAL = 'external', 'External'
    VIRTUAL = 'virtual', 'Virtual'
    ON_SITE = 'on_site', 'On Site'


class MeetingStatus(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    POSTPONED = 'postponed', 'Postponed'


class HolidayType(models.TextChoices):
    PUBLIC = 'public', 'Public'
    COMPANY = 'company', 'Company'
    REGIONAL = 'regional', 'Regional'
    OPTIONAL = 'optional', 'Optional'


class ReminderStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    SNOOZED = 'snoozed', 'Snoozed'
    DONE = 'done', 'Done'
    OVERDUE = 'overdue', 'Overdue'


class CalResourceStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    BOOKED = 'booked', 'Booked'
    MAINTENANCE = 'maintenance', 'Maintenance'
    BLOCKED = 'blocked', 'Blocked'


class BookingStatus(models.TextChoices):
    CONFIRMED = 'confirmed', 'Confirmed'
    PENDING = 'pending', 'Pending'
    CANCELLED = 'cancelled', 'Cancelled'


class SharedCalType(models.TextChoices):
    TEAM = 'team', 'Team'
    DEPARTMENT = 'department', 'Department'
    PROJECT = 'project', 'Project'
    COMPANY = 'company', 'Company'
    PERSONAL = 'personal', 'Personal'


# ---------------------------------------------------------------------------
# Calendar Event (unified feed)
# ---------------------------------------------------------------------------

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CalEventCategory.choices)
    status = models.CharField(max_length=20, choices=CalEventStatus.choices, default=CalEventStatus.UPCOMING)
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True, null=True)
    recurrence = models.CharField(max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.NONE)
    attendee_count = models.IntegerField(default=0)
    color = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source_type = models.CharField(max_length=30, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'
        ordering = ['date_start']

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

class Event(models.Model):
    code = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=EventType.choices)
    status = models.CharField(max_length=20, choices=CalEventStatus.choices, default=CalEventStatus.DRAFT)
    category = models.CharField(max_length=20, choices=CalEventCategory.choices, blank=True, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True, null=True)
    virtual_link = models.CharField(max_length=300, blank=True, null=True)
    organiser = models.CharField(max_length=150, blank=True, null=True)
    organiser_dept = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    recurrence = models.CharField(max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.NONE)
    tags = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-date_start']

    def __str__(self):
        return f"{self.code} - {self.title}"


class EventAttendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=120, blank=True, null=True)
    department = models.CharField(max_length=120, blank=True, null=True)
    status = models.CharField(max_length=20, choices=AttendeeStatus.choices, default=AttendeeStatus.PENDING)

    class Meta:
        verbose_name = 'Event Attendee'
        verbose_name_plural = 'Event Attendees'

    def __str__(self):
        return f"{self.event.code} - {self.name}"


class EventReminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    type = models.CharField(max_length=20, blank=True, null=True, help_text='email/push/sms')
    before_minutes = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = 'Event Reminder'
        verbose_name_plural = 'Event Reminders'

    def __str__(self):
        return f"{self.event.code} - {self.label}"


class EventActivity(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    user = models.CharField(max_length=150, blank=True, null=True)
    action = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Event Activity'
        verbose_name_plural = 'Event Activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event.code} - {self.action}"


# ---------------------------------------------------------------------------
# Meeting
# ---------------------------------------------------------------------------

class Meeting(models.Model):
    code = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=MeetingType.choices)
    status = models.CharField(max_length=20, choices=MeetingStatus.choices, default=MeetingStatus.SCHEDULED)
    meeting_date = models.DateField()
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    duration_min = models.IntegerField(blank=True, null=True)
    organiser = models.CharField(max_length=150, blank=True, null=True)
    organiser_dept = models.CharField(max_length=120, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    join_link = models.CharField(max_length=300, blank=True, null=True)
    mom = models.TextField(blank=True, null=True, help_text='Minutes of meeting')
    action_items = models.JSONField(default=list, blank=True)
    linked_event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='meetings',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'
        ordering = ['-meeting_date']

    def __str__(self):
        return f"{self.code} - {self.title}"


class MeetingAttendee(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendees')
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=120, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True, help_text='internal/external')
    status = models.CharField(max_length=20, choices=AttendeeStatus.choices, default=AttendeeStatus.PENDING)

    class Meta:
        verbose_name = 'Meeting Attendee'
        verbose_name_plural = 'Meeting Attendees'

    def __str__(self):
        return f"{self.meeting.code} - {self.name}"


class MeetingAgendaItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='agenda_items')
    title = models.CharField(max_length=200)
    duration_min = models.IntegerField(blank=True, null=True)
    owner = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', help_text='pending/discussed/skipped')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Meeting Agenda Item'
        verbose_name_plural = 'Meeting Agenda Items'

    def __str__(self):
        return f"{self.meeting.code} - {self.title}"


# ---------------------------------------------------------------------------
# Holiday
# ---------------------------------------------------------------------------

class Holiday(models.Model):
    name = models.CharField(max_length=150)
    holiday_date = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=HolidayType.choices)
    month = models.SmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    applicable_to = models.CharField(max_length=40, blank=True, null=True, help_text='all/UAE staff/India staff/management')
    is_optional = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'
        ordering = ['holiday_date']

    def __str__(self):
        return f"{self.name} ({self.holiday_date})"


# ---------------------------------------------------------------------------
# Reminder
# ---------------------------------------------------------------------------

class Reminder(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    due_time = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True, help_text='event/meeting/task/deadline/custom')
    status = models.CharField(max_length=20, choices=ReminderStatus.choices, default=ReminderStatus.ACTIVE)
    repeat = models.CharField(max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.NONE)
    notify_via = models.JSONField(default=list, blank=True)
    linked_to = models.CharField(max_length=200, blank=True, null=True)
    linked_id = models.IntegerField(blank=True, null=True)
    snoozed_until = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='calendar_reminders',
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'
        ordering = ['due_date']

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Calendar Resource
# ---------------------------------------------------------------------------

class CalendarResource(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, blank=True, null=True, help_text='room/equipment/vehicle/desk/studio')
    location = models.CharField(max_length=150, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CalResourceStatus.choices, default=CalResourceStatus.AVAILABLE)
    features = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Calendar Resource'
        verbose_name_plural = 'Calendar Resources'
        ordering = ['name']

    def __str__(self):
        return self.name


class ResourceBooking(models.Model):
    resource = models.ForeignKey(CalendarResource, on_delete=models.CASCADE, related_name='bookings')
    title = models.CharField(max_length=200)
    booked_by = models.CharField(max_length=150, blank=True, null=True)
    booking_date = models.DateField()
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Resource Booking'
        verbose_name_plural = 'Resource Bookings'
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.resource.name} - {self.title}"


# ---------------------------------------------------------------------------
# Shared Calendar
# ---------------------------------------------------------------------------

class SharedCalendar(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=SharedCalType.choices)
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=150, blank=True, null=True)
    owner_dept = models.CharField(max_length=120, blank=True, null=True)
    color = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=20, default='active', help_text='active/archived')
    subscriber_count = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shared Calendar'
        verbose_name_plural = 'Shared Calendars'
        ordering = ['name']

    def __str__(self):
        return self.name


class CalendarSubscription(models.Model):
    shared_calendar = models.ForeignKey(SharedCalendar, on_delete=models.CASCADE, related_name='subscriptions')
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='calendar_subscriptions')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Calendar Subscription'
        verbose_name_plural = 'Calendar Subscriptions'
        unique_together = ('shared_calendar', 'employee')

    def __str__(self):
        return f"{self.shared_calendar.name} - {self.employee}"


# ---------------------------------------------------------------------------
# Calendar Notification
# ---------------------------------------------------------------------------

class CalendarNotification(models.Model):
    type = models.CharField(max_length=20, blank=True, null=True, help_text='invite/update/cancellation/reminder/accepted/declined')
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    from_user = models.CharField(max_length=150, blank=True, null=True)
    recipient = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='calendar_notifications',
    )
    event_title = models.CharField(max_length=200, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, default='unread', help_text='unread/read')
    action_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Calendar Notification'
        verbose_name_plural = 'Calendar Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
