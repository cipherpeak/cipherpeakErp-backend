from rest_framework import serializers
from apps.task.models import Task, ServiceTaskDax, ServiceAdvantage, Mechanic, DeliveryTask
from apps.task.serializers import (
    DaxTaskListSerializer, 
    AdvantageSerializer, 
    MechanicSerializer, 
    DeliveryTaskStartDetailSerializer,
    DeliveryTaskOngoingDetailSerializer,
    DaxTaskOngoingDetailSerializer,
    AdvantageTaskOngoingDetailSerializer,
    DeliveryTodayTaskDetailSerializer,
    MechanicTaskOngoingDetailSerializer,
    MechanicTodayTaskDetailSerializer,
    DaxTodayTaskDetailSerializer,
    AdvantageTodayTaskDetailSerializer
)
from .models import *
from django.utils import timezone



class CheckInOutSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=255, required=True)
    check_date = serializers.CharField(max_length=255, required=True)
    reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    check_time = serializers.CharField(max_length=100, required=True)
    time_zone = serializers.CharField(max_length=100, required=True)

    def validate_location(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Location is required")
        return value
    
    def validate_check_date(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Check date is required")
        return value

    def validate_check_time(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Check time is required")
        return value

    def validate_time_zone(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Time zone is required")
        return value

    def validate(self, data):
        # For checkout, reason is mandatory
        if self.context.get('is_checkout', False):
            reason = data.get('reason')
            if not reason or str(reason).strip() == '':
                raise serializers.ValidationError({
                    "reason": "Reason is required for checkout"
                })
        return data
    



class BreakSerializer(serializers.Serializer):
    break_type = serializers.ChoiceField(
        choices=['lunch', 'coffee', 'stretch', 'other'],
        required=True
    )
    custom_break_type = serializers.CharField(required=False, allow_blank=True)
    duration = serializers.CharField(required=True)  
    break_start_time = serializers.CharField(required=True) 
    location = serializers.CharField(required=True)
    date = serializers.CharField(required=True)

    def validate(self, data):
        # If break_type is 'other', custom_break_type is required
        if data.get('break_type') == 'other' and not data.get('custom_break_type'):
            raise serializers.ValidationError({
                "custom_break_type": "Custom break type is required when selecting 'Other'"
            })
        return data



class EndBreakSerializer(serializers.Serializer):
    break_end_time = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
    end_reason = serializers.CharField(required=False, allow_blank=True)    



class ExtendBreakSerializer(serializers.Serializer):
    duration = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    date = serializers.CharField(required=True)




class CompanyAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAnnouncement
        fields = ['id', 'heading', 'description', 'date']    
    


class LeaveHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave
        fields = [
            'id',
            'category',
            'start_date',
            'status',
            'reason',
        ]
    


class LeaveDashboardSerializer(serializers.Serializer):
    # Top section - Days Left
    days_left = serializers.IntegerField()
    total_vacation_days = serializers.IntegerField()
    used_vacation_days = serializers.IntegerField()
    
    # Middle section - Leave counts
    leave_taken_this_month = serializers.IntegerField()
    annual_leave_taken = serializers.IntegerField()

    leave_requests = LeaveHistorySerializer(many=True)

    # Leave history (all leaves)
    leave_history = LeaveHistorySerializer(many=True)
    
    class Meta:
        fields = [
            'days_left',
            'total_vacation_days',
            'used_vacation_days',
            'leave_taken_this_month',
            'annual_leave_taken',
            'leave_requests',
            'leave_history'
        ]


import os


class LeaveCreateSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Leave.LEAVE_CATEGORY_CHOICES)
    start_date = serializers.CharField(max_length=100, required=True)
    end_date = serializers.CharField(max_length=100, required=True)
    total_days = serializers.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        min_value=0.5,
        required=False
    )
    reason = serializers.CharField(required=False, allow_blank=True)
    passport_required_from = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    passport_required_to = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    address_during_leave = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    
    attachment = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        required=False,
        write_only=True
    )
    signature = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        required=False,
        write_only=True
    )

    class Meta:
        model = Leave
        fields = [
            'category',
            'start_date',
            'end_date',
            'total_days',
            'reason',
            'passport_required_from',
            'passport_required_to',
            'address_during_leave',
            'attachment',
            'signature'
        ]

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachment', [])
        signatures_data = validated_data.pop('signature', [])
        
        leave = Leave.objects.create(**validated_data)
        
        for attachment in attachments_data:
            LeaveAttachment.objects.create(leave=leave, file=attachment)
            
        for signature in signatures_data:
            LeaveSignature.objects.create(leave=leave, file=signature)
            
        return leave
    
    def validate_total_days(self, value):
        """Validate that total_days is a positive number"""
        if value <= 0:
            raise serializers.ValidationError("Total days must be greater than 0")
        return value
    




class DetailedLeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.employee_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employeeId', read_only=True)
    approved_by_name = serializers.SerializerMethodField(read_only=True) 
    attachments = serializers.SerializerMethodField()
    signatures = serializers.SerializerMethodField()

    
    class Meta:
        model = Leave
        fields = [
            # Basic info
            'id',
            'category',
            'start_date',
            'end_date',
            'total_days',
            'reason',
            'status',
            'employee_name',
            'employee_id',
            'passport_required_from',
            'passport_required_to',
            'address_during_leave',
            'ticket_eligibility',            
            'attachments',
            'signatures',
            'approved_by_name',
            'rejection_reason',
        ]
        read_only_fields = fields
    
    def get_approved_by_name(self, obj):
        """Get the name of the approver"""
        if obj.approved_by:
            return obj.approved_by.employee_name if hasattr(obj.approved_by, 'employee_name') else str(obj.approved_by)
        return None
    
    def get_attachments(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(at.file.url) if request else at.file.url for at in obj.attachments.all()]

    def get_signatures(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(sig.file.url) if request else sig.file.url for sig in obj.signatures.all()]
    
    


# ____________________
    
from apps.dashboard.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 'created_at']


# class CheckInSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['heading', 'status', 'address', 'task_assign_time', 'percentage_completed']


class TaskSerializer(serializers.ModelSerializer):
    heading = serializers.SerializerMethodField()
    address_or_sub_details = serializers.SerializerMethodField()
    time_of_task = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'task_type', 'status', 'created_at', 'heading', 'address_or_sub_details', 'time_of_task']

    def get_heading(self, obj):
        return f"{obj.get_task_type_display()} Task"

    def get_address_or_sub_details(self, obj):
        return f"Status: {obj.get_status_display()}"

    def get_time_of_task(self, obj):
        from django.utils.timezone import localtime
        if obj.created_at:
            return localtime(obj.created_at).strftime("%d-%m-%Y %I:%M %p")
        return ""



class BreakHistorySerializer(serializers.ModelSerializer):
    number_of_extended_breaks = serializers.IntegerField(source='number_of_scheduled_breaks')
    
    class Meta:
        model = BreakHistory
        fields = ['total_break_time', 'number_of_extended_breaks']

class BreakTimerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BreakTimer
        fields = [
            'id', 
            'custom_break_type', 
            'break_type',
            'duration', 
            'break_start_time', 
            'break_end_time', 
            'date', 
            'location'
        ]

class HomeAPISerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='employee_name')  
    employee_type = serializers.CharField(read_only=True)
    company_name = serializers.SerializerMethodField()
    notification_count = serializers.SerializerMethodField()
    ongoing_task = serializers.SerializerMethodField()
    ongoing_tasks = serializers.SerializerMethodField()
    break_timer = serializers.SerializerMethodField()
    break_history = serializers.SerializerMethodField()
    status_of_check = serializers.SerializerMethodField()
    check_in_out_time = serializers.SerializerMethodField()
    total_no_of_tasks_today = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    company_announcement_details = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'name',
            'employee_type',
            'company_name',
            'notification_count',
            'ongoing_task',
            'ongoing_tasks', 
            'break_timer',
            'break_history',
            'status_of_check',
            'check_in_out_time',
            'total_no_of_tasks_today',
            'tasks',
            'company_announcement_details'
        ]

    def get_company_name(self, obj):
        return obj.company.company_name.lower() if obj.company and obj.company.company_name else ''

    def get_notification_count(self, obj):
        if hasattr(obj, 'notifications'):
            return obj.notifications.filter(is_read=False).count()
        return 0

    def get_ongoing_task(self, obj):
        """Returns True if there are any ongoing tasks, False otherwise"""
        ongoing_tasks = obj.tasks.filter(
            status__in=['paused', 'in_progress']
        )
        return ongoing_tasks.exists()

    def get_ongoing_tasks(self, obj):
        ongoing_tasks = obj.tasks.filter(
            status__in=['paused', 'in_progress']
        )
        
        # Polymorphic serialization based on employee type
        if obj.employee_type == 'office':
            return []
            
        elif obj.employee_type == 'mechanic':
            # Get related mechanic tasks
            mechanic_tasks = [t.mechanic_details for t in ongoing_tasks if hasattr(t, 'mechanic_details')]
            return MechanicTaskOngoingDetailSerializer(mechanic_tasks, many=True).data
            
        elif obj.employee_type == 'deliver':
            # Get related delivery tasks
            delivery_tasks = [t.delivery_details for t in ongoing_tasks if hasattr(t, 'delivery_details')]
            return DeliveryTaskOngoingDetailSerializer(delivery_tasks, many=True).data
            
        elif obj.employee_type == 'service':
            company_name = obj.company.company_name.lower() if obj.company and obj.company.company_name else ''
            if company_name == 'dax':
                dax_tasks = ServiceTaskDax.objects.filter(task__in=ongoing_tasks)
                return DaxTaskOngoingDetailSerializer(dax_tasks, many=True).data
                
            elif company_name == 'advantage':
                # ServiceAdvantage task=OneToOneField related_name='advantage_details'
                advantage_tasks = [t.advantage_details for t in ongoing_tasks if hasattr(t, 'advantage_details')]
                return AdvantageTaskOngoingDetailSerializer(advantage_tasks, many=True).data
        
        # Fallback for unknown types or no specific data
        return TaskSerializer(ongoing_tasks, many=True).data

    def get_break_timer(self, obj):
        today = str(timezone.localdate())
        
        # Check current status (Last record)
        last_check = obj.attendance_checks.filter(
            check_date=today
        ).order_by('created_at').last()
        
        # If currently checked out (or no record at all), hide timer
        if not last_check or last_check.check_type == 'out':
            return None

        current_break = obj.break_timers.filter(
            date=today,
            break_start_time__isnull=False
        ).last()
        
        # If the last break is finished (has end time), don't show it as active timer
        if current_break and current_break.break_end_time:
            return None
            
        return BreakTimerSerializer(current_break).data if current_break else None

    def get_break_history(self, obj):
        today = str(timezone.localdate())
        
        # Check current status (Last record)
        last_check = obj.attendance_checks.filter(
            check_date=today
        ).order_by('created_at').last()
        
        # If currently checked out (or no record), hide history?
        # User requirement seemed to be "clear when checkout", but for history maybe they want to see it?
        # The previous code was `if has_checked_out: return None`.
        # I will stick to "If currently checked out, return None" to enable it for Session 2.
        if not last_check or last_check.check_type == 'out':
            return None

        # Calculate dynamically from BreakTimer
        todays_breaks = obj.break_timers.filter(date=today)
        
        total_minutes = 0
        joined_count = todays_breaks.count()
        extended_count_sum = 0
        
        for brk in todays_breaks:
            # Sum up extensions
            extended_count_sum += brk.extend_count
            
            duration_str = brk.duration
            if duration_str:
                try:
                    # Attempt to parse common duration formats
                    # Format: "Xh Ym" or "X min" or "HH:MM"
                    
                    # Regex for "Xh Ym" or "Xh" or "Ym"
                    import re
                    hours = 0
                    minutes = 0
                    
                    # Pattern for "1h 30m" or "2h" or "45m"
                    h_match = re.search(r'(\d+)\s*h', duration_str)
                    m_match = re.search(r'(\d+)\s*m', duration_str)
                    
                    if h_match:
                        hours = int(h_match.group(1))
                    if m_match:
                        minutes = int(m_match.group(1))
                        
                    if not h_match and not m_match:
                        # Try HH:MM:SS or HH:MM
                        parts = duration_str.split(':')
                        if len(parts) == 3: # HH:MM:SS
                            hours = int(parts[0])
                            minutes = int(parts[1])
                            # ignore seconds for now
                        elif len(parts) == 2: # HH:MM
                            hours = int(parts[0])
                            minutes = int(parts[1])
                        elif len(parts) == 1 and parts[0].isdigit():
                            # Assume minutes if just a number
                            minutes = int(parts[0])
                    
                    total_minutes += (hours * 60) + minutes
                    
                except Exception:
                    # Fallback or log error parsing duration
                    pass

        # Format total_minutes back to "Xh Ym"
        total_h = total_minutes // 60
        total_m = total_minutes % 60
        formatted_total = f"{total_h}h {total_m}m"

        return {
            'total_break_time': formatted_total,
            'number_of_extended_breaks': extended_count_sum,
            'history': BreakTimerSerializer(todays_breaks, many=True).data
        }

    def get_status_of_check(self, obj):
        last_check = obj.attendance_checks.filter(
            check_date=str(timezone.localdate())
        ).order_by('created_at').last()
        
        return last_check.check_type if last_check else "out"

    def get_check_in_out_time(self, obj):
        today = str(timezone.localdate())
        today_checks = obj.attendance_checks.filter(
            check_date=today
        ).order_by('created_at')
        
        last_check = today_checks.last()
        
        # If currently checked out (or no record), clear details
        if not last_check or last_check.check_type == 'out':
            return None
        
        # If checked in, we want to show... the first check-in time? 
        # Or the current session check-in time?
        # The previous code used `check_in = today_checks.filter(check_type='in').first()`. 
        # I will stick to `first()` as "Start of Work Day".
        # If users want "Current Session Start", I should change this to `last_check` (which is 'in').
        # Given "Multiple sessions", maybe showing the LATEST check-in is more relevant for "Current Status".
        # But let's stick to `first()` to minimize behavior change beyond the bug fix.
        
        check_in = today_checks.filter(check_type='in').first()
        
        return {
            'check_in': {
                'time': check_in.check_time if check_in else None,
                'time_zone': check_in.time_zone if check_in else None,
                'location': check_in.location if check_in else None
            },
            'check_out': {
                'time': None, 
                'time_zone': None,
                'location': None,
                'reason': None
            }
        }

    def get_total_no_of_tasks_today(self, obj):
        today = timezone.localdate()
        return obj.tasks.filter(created_at__date=today).count()

    def get_tasks(self, obj):
        today = timezone.localdate()
        today_tasks = obj.tasks.filter(created_at__date=today)
        
        # Polymorphic serialization based on employee type
        if obj.employee_type == 'office':
            return []
            
        elif obj.employee_type == 'mechanic':
            mechanic_tasks = [t.mechanic_details for t in today_tasks if hasattr(t, 'mechanic_details')]
            return MechanicTodayTaskDetailSerializer(mechanic_tasks, many=True).data
            
        elif obj.employee_type == 'deliver':
            delivery_tasks = [t.delivery_details for t in today_tasks if hasattr(t, 'delivery_details')]
            return DeliveryTodayTaskDetailSerializer(delivery_tasks, many=True).data
            
        elif obj.employee_type == 'service':
            company_name = obj.company.company_name.lower() if obj.company and obj.company.company_name else ''
            if company_name == 'dax':
                dax_tasks = ServiceTaskDax.objects.filter(task__in=today_tasks)
                return DaxTodayTaskDetailSerializer(dax_tasks, many=True).data
                
            elif company_name == 'advantage':
                advantage_tasks = [t.advantage_details for t in today_tasks if hasattr(t, 'advantage_details')]
                return AdvantageTodayTaskDetailSerializer(advantage_tasks, many=True).data
            else:
                # If company is None, check individual tasks details to choose appropriate serializer
                serialized_tasks = []
                for t in today_tasks:
                    if hasattr(t, 'advantage_details'):
                        serialized_tasks.append(AdvantageTodayTaskDetailSerializer(t.advantage_details).data)
                    elif t.service_dax_tasks.exists():
                        dax_task = t.service_dax_tasks.first()
                        serialized_tasks.append(DaxTodayTaskDetailSerializer(dax_task).data)
                if serialized_tasks:
                    return serialized_tasks
        
        # Fallback
        return TaskSerializer(today_tasks, many=True).data

    def get_company_announcement_details(self, obj):
        announcements = CompanyAnnouncement.objects.filter(
            is_active=True
        ).order_by('-date')[:3]
        return CompanyAnnouncementSerializer(announcements, many=True).data


    






class MonthlyReviewSerializer(serializers.Serializer):
    # Progress Section (Based on attendance)
    monthly_progress_percentage = serializers.IntegerField()
    
    # Stats Section
    total_days_present = serializers.IntegerField()
    leave_taken = serializers.IntegerField()
    tasks_completed = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    
    # Calendar/Time Info
    current_month_name = serializers.CharField()
    current_year = serializers.IntegerField()
    current_date = serializers.CharField()
    
    # Today's Attendance Only
    todays_attendance = serializers.DictField(allow_null=True)
    
    # Leave Balance Information
    leave_balance = serializers.DictField()
