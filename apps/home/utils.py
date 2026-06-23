from django.utils import timezone
from datetime import datetime
import pytz
from rest_framework.response import Response
from rest_framework import status
from .models import AttendanceCheck, BreakTimer

def close_previous_sessions(employee):
    """
    Checks if the employee has an open session from a previous day and auto-checkouts.
    """
    last_global_attendance = AttendanceCheck.objects.filter(employee=employee).order_by('-created_at').first()
    
    if last_global_attendance and last_global_attendance.check_type == 'in':
        # Parse the check_date string to a date object for comparison
        try:
            # Try parsing the date string (assuming format YYYY-MM-DD)
            check_date_obj = datetime.strptime(last_global_attendance.check_date, '%Y-%m-%d').date()
            
            if check_date_obj < timezone.localdate():
                AttendanceCheck.objects.create(
                    employee=employee,
                    check_type='out',
                    check_date=last_global_attendance.check_date,
                    check_time="23:59:59",
                    time_zone=last_global_attendance.time_zone or "Asia/Dubai",
                    location=last_global_attendance.location or "Auto Checkout",
                    reason="Auto checkout: Midnight reached"
                )
        except (ValueError, AttributeError):
            # If parsing fails, skip the auto-checkout logic
            pass
    return

def close_previous_breaks(employee):
    """
    Checks if the employee has an open break from a previous day and auto-ends it.
    """
    active_breaks = BreakTimer.objects.filter(
        employee=employee,
        break_end_time__isnull=True
    ).exclude(date=timezone.localdate().strftime('%Y-%m-%d'))
    
    for b in active_breaks:
        b.break_end_time = "23:59:59"
        b.end_reason = "Auto end: Day changed"
        
        # Calculate duration
        try:
            start_time_str = b.break_start_time
            try:
                start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
            except ValueError:
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
            
            end_time = datetime.strptime("23:59:59", '%H:%M:%S').time()
            
            # Using current date as dummy for time difference calculation
            dummy_date = datetime.now().date()
            start_dt = datetime.combine(dummy_date, start_time)
            end_dt = datetime.combine(dummy_date, end_time)
            
            diff = end_dt - start_dt
            total_minutes = int(diff.total_seconds() / 60)
            
            h = total_minutes // 60
            m = total_minutes % 60
            b.duration = f"{h}h {m}m"
        except (ValueError, TypeError, AttributeError):
            pass
            
        b.save()
    return


def validate_employee_status(employee, action_verb):
    """
    Helper to validate if an employee is allowed to perform an action (like note/task operations).
    Returns (True, None) if allowed, or (False, Response) if blocked.
    """
    # 0. Ensure no open sessions from previous days
    close_previous_sessions(employee)
    close_previous_breaks(employee)

    # 1. Check Attendance
    last_attendance = AttendanceCheck.objects.filter(
        employee=employee,
        check_date=timezone.localdate()
    ).order_by('-created_at').first()

    # Auto-Checkout / Time Constraint Logic
    # Removed as per requirement to allow 24hr working time.
    # The system will rely on close_previous_sessions for midnight reset.

    # If no record today, or last record is check-out, then user is NOT checked in
    if not last_attendance or last_attendance.check_type == 'out':
        return False, Response({
            "success": False,
            "error": f"Please check in first before {action_verb}"
        }, status=status.HTTP_403_FORBIDDEN)

    # 2. Check for Active Break
    active_break = BreakTimer.objects.filter(
        employee=employee,
        break_end_time__isnull=True
    ).exists()

    if active_break:
        return False, Response({
            "success": False,
            "error": f"You cannot {action_verb} while on a break. Please end your break first."
        }, status=status.HTTP_403_FORBIDDEN)

    return True, None
