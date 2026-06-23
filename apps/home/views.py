# views.py
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import AttendanceCheck, BreakHistory, BreakTimer, CompanyAnnouncement, Employee, Leave, ExtendBreak, LeaveBalance
from .serializers import BreakSerializer, CheckInOutSerializer, CompanyAnnouncementSerializer, DetailedLeaveSerializer, EndBreakSerializer, HomeAPISerializer, LeaveCreateSerializer, LeaveDashboardSerializer, LeaveHistorySerializer
from django.shortcuts import get_object_or_404
from apps.dashboard.models import Notification
from .serializers import NotificationSerializer
from django.db.models import Q, Sum
from calendar import monthrange
import calendar
from datetime import datetime
from apps.task.models import Task
from .serializers import MonthlyReviewSerializer
from .utils import validate_employee_status, close_previous_sessions, close_previous_breaks


class CheckInAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            employee = request.user
            # Ensure no open sessions/breaks from previous days
            close_previous_sessions(employee)
            close_previous_breaks(employee)

            serializer = CheckInOutSerializer(data=request.data, context={'is_checkout': False})
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            employee = request.user
            check_date = serializer.validated_data['check_date']

            # Time Constraint Check (New)
            try:
                check_in_time_str = serializer.validated_data['check_time']
                # Try parsing with seconds first, then without
                try:
                    check_in_time_obj = datetime.strptime(check_in_time_str, '%H:%M:%S').time()
                except ValueError:
                    check_in_time_obj = datetime.strptime(check_in_time_str, '%H:%M').time()
                
                # Time Constraint Check removed as per requirement (24hr allowed)
                pass
            except ValueError:
                pass

            # Check the LAST attendance record for today (or overall if needed, but today is sufficient for daily reset logic)
            last_record = AttendanceCheck.objects.filter(
                employee=employee,
                check_date=check_date
            ).order_by('created_at').last()
            
            # If last record exists and is 'in', deny check-in
            if last_record and last_record.check_type == 'in':
                return Response(
                    {"error": "You are already checked in. Please check out first."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 3. Chronological Failure Check (New Requirement)
            # If last record exists (which must be 'out' at this point), ensure new check-in is AFTER that check-out
            if last_record and last_record.check_type == 'out':
                try:
                    current_time_str = serializer.validated_data['check_time']
                    last_time_str = last_record.check_time
                    
                    # Parse times
                    # Try with seconds
                    try:
                        current_dt = datetime.strptime(current_time_str, '%H:%M:%S').time()
                    except ValueError:
                        current_dt = datetime.strptime(current_time_str, '%H:%M').time()
                        
                    try:
                        last_dt = datetime.strptime(last_time_str, '%H:%M:%S').time()
                    except ValueError:
                        last_dt = datetime.strptime(last_time_str, '%H:%M').time()
                    
                    if current_dt <= last_dt:
                        return Response(
                            {"error": f"Check-in time ({current_time_str}) cannot be earlier than or equal to the last check-out time ({last_time_str})."}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except ValueError:
                    # If parsing fails, we might skip validation or log error, but for now let's be safe
                    pass
            
            reason = serializer.validated_data.get('reason')
            
            reason_to_store = reason if reason and str(reason).strip() != '' else None
            
            checkin = AttendanceCheck.objects.create(
                employee=employee,
                check_type='in',
                check_date=check_date,                 
                check_time=serializer.validated_data['check_time'],
                time_zone=serializer.validated_data['time_zone'],
                location=serializer.validated_data['location'],
                reason=reason_to_store,
            )
            
            return Response({
                "status": "success",
                "message": "Checked in successfully",
                "check_id": checkin.id,
                "check_date": checkin.check_date,
                "check_time": checkin.check_time,
                "time_zone": checkin.time_zone,
                "location": checkin.location,
                "reason_provided": reason_to_store is not None 
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class CheckOutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = CheckInOutSerializer(data=request.data, context={'is_checkout': True})
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            employee = request.user
            check_date = serializer.validated_data['check_date']

            # Check the LAST attendance record for today
            last_record = AttendanceCheck.objects.filter(
                employee=employee,
                check_date=check_date
            ).order_by('created_at').last()
            
            # If no record today or last record is 'out', deny check-out
            if not last_record or last_record.check_type == 'out':
                return Response(
                    {"error": "You need to check in first"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Chronological Check for Checkout
            if last_record and last_record.check_type == 'in':
                try:
                    current_time_str = serializer.validated_data['check_time']
                    last_time_str = last_record.check_time
                    
                    # Parse times
                    try:
                        current_dt = datetime.strptime(current_time_str, '%H:%M:%S').time()
                    except ValueError:
                        current_dt = datetime.strptime(current_time_str, '%H:%M').time()
                        
                    try:
                        last_dt = datetime.strptime(last_time_str, '%H:%M:%S').time()
                    except ValueError:
                        last_dt = datetime.strptime(last_time_str, '%H:%M').time()
                    
                    if current_dt <= last_dt:
                         return Response(
                            {"error": f"Check-out time ({current_time_str}) cannot be earlier than or equal to the check-in time ({last_time_str})."}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except ValueError:
                    pass
            
            active_break = BreakTimer.objects.filter(
                employee=employee,
                break_end_time__isnull=True
            ).exists()
            
            if active_break:
                return Response(
                    {"error": "Please end your break before checking out"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create check-out record WITH reason (mandatory)
            checkout = AttendanceCheck.objects.create(
                employee=employee,
                check_type='out',
                check_date=serializer.validated_data['check_date'],
                check_time=serializer.validated_data['check_time'],
                time_zone=serializer.validated_data['time_zone'],
                location=serializer.validated_data['location'],
                reason=serializer.validated_data['reason']  
            )
            
            # The following variables are not defined in the original context,
            # assuming they would be defined elsewhere in a complete implementation
            # or are placeholders for future logic.
            check_out_time = checkout.check_time # Example, assuming this is the intended value
            checkout_reason = checkout.reason # Example, assuming this is the intended value
            status_text = "completed" # Example, assuming this is the intended value

            return Response({
                "status": "success",
                "message": "Checked out successfully",
                "check_id": checkout.id,
                "check_date": checkout.check_date,
                "check_time": checkout.check_time,
                'check_out_time': check_out_time,
                'checkout_reason': checkout_reason,
                'status': status_text
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class StartBreakAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BreakSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = request.user
        close_previous_breaks(employee)
        today = serializer.validated_data['date']

        # Validate Active Session
        last_attendance = AttendanceCheck.objects.filter(
            employee=employee,
            check_date=today
        ).order_by('created_at').last()

        # Must be checked in to start a break
        if not last_attendance or last_attendance.check_type == 'out':
            return Response(
                {"error": "You need to check in first before starting a break"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if BreakTimer.objects.filter(
            employee=employee,
            date=today,
            break_end_time__isnull=True
        ).exists():
            return Response(
                {"error": "You already have an active break"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Chronological Validation: Start time must be after last completed break's end time
        last_completed_break = BreakTimer.objects.filter(
            employee=employee,
            date=today,
            break_end_time__isnull=False
        ).order_by('id').last()
        
        if last_completed_break:
            try:
                new_start_str = serializer.validated_data['break_start_time']
                last_end_str = last_completed_break.break_end_time
                
                try:
                    new_start_time = datetime.strptime(new_start_str, '%H:%M:%S').time()
                except ValueError:
                    new_start_time = datetime.strptime(new_start_str, '%H:%M').time()
                    
                try:
                    last_end_time = datetime.strptime(last_end_str, '%H:%M:%S').time()
                except ValueError:
                    last_end_time = datetime.strptime(last_end_str, '%H:%M').time()
                    
                if new_start_time <= last_end_time:
                     return Response(
                        {"error": f"Break start time ({new_start_str}) cannot be earlier than or equal to the last break end time ({last_end_str})."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                pass
                
        # Also validate start time is after current check-in time?
        # User didn't ask explicitly but it makes sense check-in time < break start time.
        # last_attendance is presumably the 'in' record.
        if last_attendance and last_attendance.check_type == 'in':
             try:
                new_start_str = serializer.validated_data['break_start_time']
                checkin_time_str = last_attendance.check_time
                
                try:
                    new_start_time = datetime.strptime(new_start_str, '%H:%M:%S').time()
                except ValueError:
                    new_start_time = datetime.strptime(new_start_str, '%H:%M').time()
                
                try:
                    checkin_time = datetime.strptime(checkin_time_str, '%H:%M:%S').time()
                except ValueError:
                    checkin_time = datetime.strptime(checkin_time_str, '%H:%M').time()
                    
                if new_start_time <= checkin_time:
                    return Response(
                        {"error": f"Break start time ({new_start_str}) cannot be earlier than or equal to the current check-in time ({checkin_time_str})."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
             except ValueError:
                 pass

        break_data = {
            'employee': employee,
            'break_type': serializer.validated_data['break_type'],
            'duration': serializer.validated_data['duration'],
            'break_start_time': serializer.validated_data['break_start_time'],
            'date': today,
            'location': serializer.validated_data['location'],
        }

        if serializer.validated_data['break_type'] == 'other':
            break_data['custom_break_type'] = serializer.validated_data.get('custom_break_type')

        BreakTimer.objects.create(**break_data)

        return Response({
            "status": "success",
            "message": "Break started successfully",
        }, status=status.HTTP_201_CREATED)



class EndBreakAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EndBreakSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = request.user
        today = serializer.validated_data['date']

        # Validate Active Session (Safety check)
        # Technically if they have an active break, they should be checked in, but good to double check status hasn't drifted
        last_attendance = AttendanceCheck.objects.filter(
            employee=employee,
            check_date=today
        ).order_by('created_at').last()

        if not last_attendance or last_attendance.check_type == 'out':
             return Response(
                {"error": "You are checked out. Please check in first."},
                status=status.HTTP_400_BAD_REQUEST
            )

        active_break = BreakTimer.objects.filter(
            employee=employee,
            date=today,
            break_end_time__isnull=True
        ).first()

        if not active_break:
            return Response(
                {"error": "No active break found"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Validate End Time vs Start Time
        try:
            end_time_str = serializer.validated_data['break_end_time']
            start_time_str = active_break.break_start_time
            
            try:
                end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
            except ValueError:
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
            try:
                start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
            except ValueError:
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                
            if end_time <= start_time:
                 return Response(
                    {"error": f"Break end time ({end_time_str}) cannot be earlier than or equal to the break start time ({start_time_str})."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            

            # Calculate and update actual duration
            dummy_date = datetime.now().date()
            start_dt = datetime.combine(dummy_date, start_time)
            end_dt = datetime.combine(dummy_date, end_time)
            
            diff = end_dt - start_dt
            total_minutes = int(diff.total_seconds() / 60)
            
            h = total_minutes // 60
            m = total_minutes % 60
            active_break.duration = f"{h}h {m}m"
        except ValueError:
            pass

        reason = serializer.validated_data.get('end_reason')
        active_break.break_end_time = serializer.validated_data['break_end_time']
        active_break.end_reason = reason.strip() if reason and reason.strip() else None
        active_break.location = serializer.validated_data['location']
        active_break.save()

        return Response({
            "status": "success",
            "message": "Break ended successfully",
        }, status=status.HTTP_200_OK)



class ExtendBreakAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from .serializers import ExtendBreakSerializer 
        
        serializer = ExtendBreakSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = request.user
        today = serializer.validated_data['date']

        active_break = BreakTimer.objects.filter(
            employee=employee,
            date=today,
            break_end_time__isnull=True
        ).last()

        if not active_break:
            return Response(
                {"error": "No active break found to extend"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Create ExtendBreak record linked to the active break
        ExtendBreak.objects.create(
            break_timer=active_break,
            duration=serializer.validated_data['duration'],
            location=serializer.validated_data['location'],
            date=serializer.validated_data['date']
        )
        
        # Parse existing duration
        existing_duration_str = active_break.duration
        new_duration_str = serializer.validated_data['duration']
        
        # Helper to parse minutes
        def parse_to_minutes(d_str):
            if not d_str: return 0
            import re
            mins = 0
            try:
                h_match = re.search(r'(\d+)\s*h', d_str)
                m_match = re.search(r'(\d+)\s*m', d_str)
                if h_match: mins += int(h_match.group(1)) * 60
                if m_match: mins += int(m_match.group(1))
                if not h_match and not m_match:
                     if ':' in d_str:
                         p = d_str.split(':')
                         if len(p) == 3: mins += int(p[0])*60 + int(p[1])
                         elif len(p) == 2: mins += int(p[0])*60 + int(p[1])
                     elif d_str.isdigit():
                         mins += int(d_str)
            except: pass
            return mins

        total_minutes = parse_to_minutes(existing_duration_str) + parse_to_minutes(new_duration_str)
        
        # Format back to "Xh Ym"
        h = total_minutes // 60
        m = total_minutes % 60
        formatted_duration = f"{h}h {m}m"
        
        active_break.duration = formatted_duration
        active_break.location = serializer.validated_data['location']
        active_break.extend_count += 1
        active_break.save()

        return Response({
            "status": "success",
            "message": "Break extended successfully",
            "new_duration": formatted_duration,
            "extend_count": active_break.extend_count
        }, status=status.HTTP_200_OK)



class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            employee = request.user
            serializer = HomeAPISerializer(employee)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]


class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            
            query = Q(recipient=user) | Q(target_all=True)
            
            if user.company:
                query |= Q(target_company=user.company)
            
            if user.employee_type:
                query |= Q(target_department=user.employee_type)

            notifications = Notification.objects.filter(query).order_by('-created_at')
            
            # Optional filtering by type
            notif_type = request.query_params.get('type')
            if notif_type:
                notifications = notifications.filter(notification_type=notif_type)
            
            serializer = NotificationSerializer(notifications, many=True)
            return Response({
                "success": True, 
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False, 
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CompanyAnnouncementListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            announcements = CompanyAnnouncement.objects.filter(
                is_active=True
            ).order_by('-date')
            
            serializer = CompanyAnnouncementSerializer(announcements, many=True)
            
            return Response({
                'status': 'success',
                'count': announcements.count(),
                'announcements': serializer.data
            })
            
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )            
        

import pytz
from datetime import timedelta
from django.db.models import Q, Sum

class LeaveDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get employee profile from authenticated user
            employee = request.user
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Set Dubai timezone
        dubai_tz = pytz.timezone('Asia/Dubai')
        now_dubai = timezone.now().astimezone(dubai_tz)
        
        # Calculate current month start and end in Dubai timezone
        current_month_start = now_dubai.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Get all leaves for the employee
        all_leaves = Leave.objects.filter(employee=employee)
        
        # 1. Calculate days left (assuming 30 days total vacation)
        total_vacation_days = 30  # This could be configured per employee
        
        # Calculate used vacation days (only approved leaves)
        approved_leaves = all_leaves.filter(
            status='approved',
            category='annual'  
        )
        print(approved_leaves, "approved")
        used_vacation_days = approved_leaves.aggregate(
            total=Sum('total_days')
        )['total'] or 0
        print(used_vacation_days, "vacation")
        days_left = total_vacation_days - used_vacation_days
        print(days_left, "vacation")

        # 2. Calculate leave taken this month (all categories, approved only)
        leave_this_month = all_leaves.filter(
            status='approved',
            created_at__gte=current_month_start,
            created_at__lte=current_month_end
        )
        leave_taken_this_month_count = leave_this_month.count()
        
        # 3. Calculate annual leave taken (approved annual leaves)
        annual_leave_taken_count = all_leaves.filter(
            status='approved',
            category='annual'
        ).count()
        
        # 4. Get recent leave requests (last 5, sorted by created date)
        # Only show PENDING requests in leave_requests section
        recent_requests = all_leaves.filter(
            status='pending'
        ).order_by('-created_at')[:5]
        
        # 5. Get all leave history
        # Show only APPROVED, REJECTED, or CANCELLED leaves in history (not pending)
        all_history = all_leaves.filter(
            Q(status='approved') | Q(status='rejected') | Q(status='cancelled')
        ).order_by('-created_at')
        
        # Serialize the data
        dashboard_data = {
            'days_left': days_left,
            'total_vacation_days': total_vacation_days,
            'used_vacation_days': used_vacation_days,
            'leave_taken_this_month': leave_taken_this_month_count,
            'annual_leave_taken': annual_leave_taken_count,
            'leave_requests': recent_requests,  # Only pending
            'leave_history': all_history  # Only non-pending (approved/rejected/cancelled)
        }
        
        serializer = LeaveDashboardSerializer(dashboard_data)
        return Response(serializer.data)
    


class LeaveDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, leave_id):
        try:
            # Get the authenticated user's employee profile
            employee = request.user
            
            # Get the specific leave for this employee
            leave = get_object_or_404(Leave, id=leave_id, employee=employee)
            
            # Serialize the leave data
            serializer = DetailedLeaveSerializer(leave, context={'request': request})
            
            return Response({
                "success": True,
                "message": "Leave details retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Employee.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Employee profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Leave.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Leave application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )



from rest_framework.parsers import MultiPartParser, FormParser


class LeaveApplicationView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        try:
            employee = request.user
        except Employee.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Employee profile not found. Please complete your profile."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if employee is active
        if not employee.is_active:
            return Response(
                {
                    "success": False,
                    "error": "Your account is not active. Please contact HR."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use a copy of request.data to handle multiple file uploads
        data = request.data.copy()
        
        # Ensure 'attachment' and 'signature' are handled as lists of files
        if 'attachment' in request.FILES:
            data.setlist('attachment', request.FILES.getlist('attachment'))
        if 'signature' in request.FILES:
            data.setlist('signature', request.FILES.getlist('signature'))
            
        serializer = LeaveCreateSerializer(data=data)
        
        if serializer.is_valid():
            # Create the leave application
            try:
                leave = serializer.save(
                    employee=employee,
                    status='pending'  # Default status
                )
                
                return Response({
                    "success": True,
                    "message": "Leave application submitted successfully!",
                    "next_steps": "Your leave application is pending approval. You will be notified once it's reviewed."
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    "success": False,
                    "error": f"Error creating leave application: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            # Return validation errors
            errors = serializer.errors
            
            # Format errors for better readability
            formatted_errors = {}
            for field, error_list in errors.items():
                if isinstance(error_list, list):
                    formatted_errors[field] = error_list[0] if error_list else "Invalid value"
                else:
                    formatted_errors[field] = str(error_list)
            
            return Response({
                "success": False,
                "error": "Validation failed",
                "details": formatted_errors
            }, status=status.HTTP_400_BAD_REQUEST)


def calculate_leave_balance(employee, year, month):
    """
    Calculate leave balance for an employee for a specific year/month
    Monthly accrual system with simple calculation (no prorating)
    - 2.5 days accrued each month
    - Carry forward from previous months within same year
    - Annual carry forward from previous year (max 30 days, only 1 year)
    - Full leave days counted in month when leave starts (no prorating)
    """
    from datetime import date as dt_date
    from decimal import Decimal
    
    MONTHLY_ACCRUAL = Decimal('2.5')
    ANNUAL_CARRY_LIMIT = Decimal('30')
    
    # Get or create balance for current month
    balance, created = LeaveBalance.objects.get_or_create(
        employee=employee,
        year=year,
        month=month,
        defaults={
            'monthly_accrued': MONTHLY_ACCRUAL,
            'carried_forward': 0,
            'total_available': MONTHLY_ACCRUAL,
            'used': 0,
            'remaining': MONTHLY_ACCRUAL
        }
    )
    
    # Calculate carry forward from previous months in same year
    carry_forward = Decimal('0')
    previous_balances = LeaveBalance.objects.filter(
        employee=employee,
        year=year,
        month__lt=month
    ).order_by('-month')
    
    for prev_balance in previous_balances:
        carry_forward += prev_balance.remaining
    
    # Annual carry forward from previous year (only in January, max 30 days, 1 year only)
    if month == 1:
        prev_year = year - 1
        dec_balance = LeaveBalance.objects.filter(
            employee=employee,
            year=prev_year,
            month=12
        ).first()
        
        if dec_balance:
            annual_carry = min(dec_balance.remaining, ANNUAL_CARRY_LIMIT)
            carry_forward += annual_carry
    
    # Calculate used leave - SIMPLE: count full leave days if leave starts in this month
    used_leave = Decimal('0')
    approved_leaves = Leave.objects.filter(
        employee=employee,
        status='approved'
    )
    
    for leave in approved_leaves:
        try:
            leave_start = dt_date.fromisoformat(leave.start_date)
            # Simple: if leave starts in this month/year, count full days
            if leave_start.year == year and leave_start.month == month:
                used_leave += (leave.total_days or Decimal('0'))
        except (ValueError, TypeError):
            pass
    
    # Simple calculation
    total_available = MONTHLY_ACCRUAL + carry_forward
    remaining = total_available - used_leave
    
    # Update balance
    balance.monthly_accrued = MONTHLY_ACCRUAL
    balance.carried_forward = carry_forward
    balance.total_available = total_available
    balance.used = used_leave
    balance.remaining = remaining
    balance.save()
    
    return {
        'current_month_balance': float(remaining),
        'total_available_leave': float(remaining),
        'monthly_accrued': float(MONTHLY_ACCRUAL),
        'carried_forward': float(carry_forward),
        'used_this_month': float(used_leave),
        'year': year,
        'month': month,
    }


class MonthlyReviewView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            employee = request.user
            
            # Setup Timezones
            dubai_tz = pytz.timezone('Asia/Dubai')
            now_dubai = timezone.now().astimezone(dubai_tz)
            
            # Get month/year from query params or default to current (Dubai time)
            try:
                month = int(request.query_params.get('month', now_dubai.month))
                year = int(request.query_params.get('year', now_dubai.year))
            except ValueError:
                month = now_dubai.month
                year = now_dubai.year
                
            # Date range for the query (Dubai time)
            # Create timezone-aware datetime for start/end
            start_date = dubai_tz.localize(datetime(year, month, 1, 0, 0, 0))
            _, last_day = monthrange(year, month)
            end_date = dubai_tz.localize(datetime(year, month, last_day, 23, 59, 59))

            # --- 1. Attendance Statistics ---
            # Filter check-ins for this month
            # Assuming 'YYYY-MM-DD' format stored in CharField
            month_str = f"{year}-{month:02d}"
            monthly_checks = AttendanceCheck.objects.filter(
                employee=employee,
                check_date__startswith=month_str
            )

            # Count unique days present (days with at least one 'in' check)
            present_dates = monthly_checks.filter(check_type='in').values_list('check_date', flat=True).distinct()
            total_days_present = present_dates.count()
            # --- 2. Leave Statistics ---
            approved_leaves = Leave.objects.filter(
                employee=employee,
                status='approved'
            )
            
            leave_taken_count = 0
            
            def parse_date(d_str):
                try:
                    return datetime.strptime(d_str, '%Y-%m-%d').date()
                except:
                    return None

            query_start_date = start_date.date()
            query_end_date = end_date.date()

            for leave in approved_leaves:
                l_start = parse_date(leave.start_date)
                l_end = parse_date(leave.end_date)
                
                if l_start and l_end:
                    latest_start = max(l_start, query_start_date)
                    earliest_end = min(l_end, query_end_date)
                    
                    if latest_start <= earliest_end:
                        delta = (earliest_end - latest_start).days + 1
                        leave_taken_count += delta

            # --- 3. Task Statistics ---
            tasks_completed = 0
            pending_tasks = 0
            
            if employee.employee_type != 'office':
                month_tasks = Task.objects.filter(
                    employee=employee,
                    created_at__year=year,
                    created_at__month=month
                )
                
                tasks_completed = month_tasks.filter(
                    status__in=['completed', 'delivered', 'returned']
                ).count()
                
                pending_tasks = month_tasks.exclude(
                    status__in=['completed', 'delivered', 'returned']
                ).count()

            # --- 4. Monthly Progress (Attendance Based) ---
            # Progress = (Days Present / Working Days So Far) * 100
            # Excluding Sundays as non-working days
            
            days_passed_in_month = (min(now_dubai, end_date) - start_date).days + 1
            if days_passed_in_month < 0: days_passed_in_month = 0 # Future month
            
            working_days_so_far = 0
            curr = start_date
            limit = min(now_dubai, end_date)

            # If looking at past month, limit is end_date
            if now_dubai > end_date:
                limit = end_date

            target_limit_date = limit.date()
            loop_date = start_date.date()
            
            while loop_date <= target_limit_date:
                if loop_date.weekday() != 6: # Not Sunday
                    working_days_so_far += 1
                loop_date += timedelta(days=1)
            
            if working_days_so_far > 0:
                progress = int((total_days_present / working_days_so_far) * 100)
                if progress > 100: progress = 100
            else:
                progress = 0
            
            # --- 5. Today's Attendance Details ---
            todays_attendance = None
            today_str = now_dubai.strftime('%Y-%m-%d')
            
            # Check if requested month is current month to show today's details?
            # User requirement: "just i want to todays attendence details" -> seemingly always return today's status
            
            today_checks = AttendanceCheck.objects.filter(
                employee=employee,
                check_date=today_str
            ).order_by('created_at')
            
            check_in = today_checks.filter(check_type='in').first()
            check_out = today_checks.filter(check_type='out').last()
            
            if check_in:
                todays_attendance = {
                     'check_in_time': check_in.check_time,
                     'check_out_time': check_out.check_time if check_out else None,
                     'checkout_reason': check_out.reason if check_out else None,
                     'status': 'Present'
                }
            else:
                 todays_attendance = {
                     'check_in_time': None,
                     'check_out_time': None,
                     'checkout_reason': None,
                     'status': 'Absent' 
                 }

            # Calculate leave balance for the current month/year
            leave_balance_data = calculate_leave_balance(employee, year, month)

            serializer = MonthlyReviewSerializer({
                'monthly_progress_percentage': progress,
                'total_days_present': total_days_present,
                'leave_taken': leave_taken_count,
                'tasks_completed': tasks_completed,
                'pending_tasks': pending_tasks,
                'current_month_name': calendar.month_name[month],
                'current_year': year,
                'current_date': now_dubai.strftime('%d'),
                'todays_attendance': todays_attendance,
                'leave_balance': leave_balance_data
            })
            
            
            return Response(serializer.data)
            
        except Exception as e:
            # print(e)
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            employee = request.user
            data = request.data
            
            # Expecting date, month, year in payload
            day = data.get('date')
            month = data.get('month')
            year = data.get('year')
            
            if not all([day, month, year]):
                return Response(
                    {"error": "Please provide date, month, and year"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Construct date string "YYYY-MM-DD"
            # Assuming input can be int or str
            try:
                # Convert to integers and validate
                day_int = int(day)
                month_int = int(month)
                year_int = int(year)
                
                # Basic validation
                if not (1 <= day_int <= 31):
                    raise ValueError("Day must be between 1 and 31")
                if not (1 <= month_int <= 12):
                    raise ValueError("Month must be between 1 and 12")
                if year_int < 1900 or year_int > 2100:
                    raise ValueError("Year must be between 1900 and 2100")
                
                query_date = f"{year_int}-{month_int:02d}-{day_int:02d}"
            except (ValueError, TypeError) as e:
                return Response(
                    {"error": f"Invalid date format: {str(e)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Fetch attendance for this date
            checks = AttendanceCheck.objects.filter(
                employee=employee,
                check_date=query_date
            ).order_by('created_at')
            
            attendance_history = []
            for check in checks:
                attendance_history.append({
                    "id": check.id,
                    "type": check.check_type,
                    "time": check.check_time if check.check_time else "",
                    "reason": check.reason if check.reason else "",
                    "location": check.location if check.location else ""
                })
            
            # Determine overall status (Present if at least one check-in exists)
            is_present = checks.filter(check_type='in').exists()
            
            response_data = {
                'status': 'Present' if is_present else 'Absent',
                'date': query_date,
                'history': attendance_history
            }
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {"error": f"Server error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TodayAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        employee = request.user
        dubai_tz = pytz.timezone('Asia/Dubai')
        now_dubai = timezone.now().astimezone(dubai_tz)
        today_str = now_dubai.strftime('%Y-%m-%d')
        
        # Get checks for today
        today_checks = AttendanceCheck.objects.filter(
            employee=employee,
            check_date=today_str
        ).order_by('created_at')
        
        if not today_checks.exists():
            return Response({
                "id": 0,
                "date": today_str,
                "check_in_at": None,
                "check_out_at": None,
                "location": None,
                "status": "absent",
                "worked_minutes": 0,
                "break_minutes": 0,
                "active_break_start_time": None,
                "notes": None
            }, status=status.HTTP_200_OK)
            
        first_in = today_checks.filter(check_type='in').first()
        last_check = today_checks.last()
        
        if not first_in:
            return Response({
                "id": 0,
                "date": today_str,
                "check_in_at": None,
                "check_out_at": None,
                "location": None,
                "status": "absent",
                "worked_minutes": 0,
                "break_minutes": 0,
                "active_break_start_time": None,
                "notes": None
            }, status=status.HTTP_200_OK)
            
        # Determine status and get active break
        active_break = BreakTimer.objects.filter(
            employee=employee,
            date=today_str,
            break_end_time__isnull=True
        ).first()
        
        if last_check.check_type == 'out':
            current_status = 'checked_out'
        else:
            current_status = 'on_break' if active_break is not None else 'present'
            
        # Calculate break minutes (total completed breaks)
        break_mins = 0
        todays_breaks = BreakTimer.objects.filter(employee=employee, date=today_str)
        for b in todays_breaks:
            if b.break_end_time:
                try:
                    b_start = datetime.strptime(b.break_start_time, '%H:%M:%S').time()
                    b_end = datetime.strptime(b.break_end_time, '%H:%M:%S').time()
                except ValueError:
                    try:
                        b_start = datetime.strptime(b.break_start_time, '%H:%M').time()
                        b_end = datetime.strptime(b.break_end_time, '%H:%M').time()
                    except ValueError:
                        continue
                b_start_dt = datetime.combine(now_dubai.date(), b_start)
                b_end_dt = datetime.combine(now_dubai.date(), b_end)
                b_diff = b_end_dt - b_start_dt
                break_mins += int(b_diff.total_seconds() / 60)
            
        # Calculate worked minutes
        worked_mins = 0
        try:
            # Try parsing first check_in_time
            in_time_obj = datetime.strptime(first_in.check_time, '%H:%M:%S').time()
        except ValueError:
            try:
                in_time_obj = datetime.strptime(first_in.check_time, '%H:%M').time()
            except ValueError:
                in_time_obj = None
                
        if in_time_obj:
            today_date = now_dubai.date()
            start_dt = datetime.combine(today_date, in_time_obj)
            
            if last_check.check_type == 'out':
                try:
                    out_time_obj = datetime.strptime(last_check.check_time, '%H:%M:%S').time()
                except ValueError:
                    try:
                        out_time_obj = datetime.strptime(last_check.check_time, '%H:%M').time()
                    except ValueError:
                        out_time_obj = None
                if out_time_obj:
                    end_dt = datetime.combine(today_date, out_time_obj)
                else:
                    end_dt = start_dt
            else:
                end_dt = now_dubai.replace(tzinfo=None)
                
            diff = end_dt - start_dt
            worked_mins = max(0, int(diff.total_seconds() / 60))
            
            # Subtract breaks from today
            for b in todays_breaks:
                if b.break_end_time:
                    try:
                        b_start = datetime.strptime(b.break_start_time, '%H:%M:%S').time()
                        b_end = datetime.strptime(b.break_end_time, '%H:%M:%S').time()
                    except ValueError:
                        try:
                            b_start = datetime.strptime(b.break_start_time, '%H:%M').time()
                            b_end = datetime.strptime(b.break_end_time, '%H:%M').time()
                        except ValueError:
                            continue
                    b_start_dt = datetime.combine(today_date, b_start)
                    b_end_dt = datetime.combine(today_date, b_end)
                    b_diff = b_end_dt - b_start_dt
                    worked_mins -= int(b_diff.total_seconds() / 60)
                elif current_status == 'on_break':
                    try:
                        b_start = datetime.strptime(b.break_start_time, '%H:%M:%S').time()
                    except ValueError:
                        try:
                            b_start = datetime.strptime(b.break_start_time, '%H:%M').time()
                        except ValueError:
                            continue
                    b_start_dt = datetime.combine(today_date, b_start)
                    b_diff = now_dubai.replace(tzinfo=None) - b_start_dt
                    worked_mins -= int(b_diff.total_seconds() / 60)
                    
            worked_mins = max(0, worked_mins)

        return Response({
            "id": first_in.id,
            "date": first_in.check_date,
            "check_in_at": first_in.check_time,
            "check_out_at": last_check.check_time if last_check.check_type == 'out' else None,
            "location": first_in.location,
            "status": current_status,
            "worked_minutes": worked_mins,
            "break_minutes": break_mins,
            "active_break_start_time": active_break.break_start_time if active_break else None,
            "notes": first_in.reason
        }, status=status.HTTP_200_OK)


class AttendanceHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        employee = request.user
        limit = request.query_params.get('limit')
        
        # Get unique check_dates for this employee
        dates = AttendanceCheck.objects.filter(employee=employee).values_list('check_date', flat=True).distinct().order_by('-check_date')
        
        if limit:
            try:
                dates = dates[:int(limit)]
            except ValueError:
                pass
                
        results = []
        for check_date in dates:
            checks = AttendanceCheck.objects.filter(employee=employee, check_date=check_date).order_by('created_at')
            first_in = checks.filter(check_type='in').first()
            last_out = checks.filter(check_type='out').last()
            
            if not first_in:
                continue
                
            # Compute worked minutes
            worked_mins = 0
            try:
                in_time = datetime.strptime(first_in.check_time, '%H:%M:%S').time()
            except ValueError:
                try:
                    in_time = datetime.strptime(first_in.check_time, '%H:%M').time()
                except ValueError:
                    in_time = None
                    
            if in_time:
                try:
                    today_date = datetime.strptime(check_date, '%Y-%m-%d').date()
                except ValueError:
                    continue
                start_dt = datetime.combine(today_date, in_time)
                if last_out:
                    try:
                        out_time = datetime.strptime(last_out.check_time, '%H:%M:%S').time()
                    except ValueError:
                        try:
                            out_time = datetime.strptime(last_out.check_time, '%H:%M').time()
                        except ValueError:
                            out_time = None
                    if out_time:
                        end_dt = datetime.combine(today_date, out_time)
                    else:
                        end_dt = start_dt
                else:
                    end_dt = start_dt
                
                diff = end_dt - start_dt
                worked_mins = max(0, int(diff.total_seconds() / 60))
                
                # Subtract breaks
                breaks = BreakTimer.objects.filter(employee=employee, date=check_date)
                for b in breaks:
                    if b.break_end_time:
                        try:
                            b_start = datetime.strptime(b.break_start_time, '%H:%M:%S').time()
                            b_end = datetime.strptime(b.break_end_time, '%H:%M:%S').time()
                        except ValueError:
                            try:
                                b_start = datetime.strptime(b.break_start_time, '%H:%M').time()
                                b_end = datetime.strptime(b.break_end_time, '%H:%M').time()
                            except ValueError:
                                continue
                        b_start_dt = datetime.combine(today_date, b_start)
                        b_end_dt = datetime.combine(today_date, b_end)
                        b_diff = b_end_dt - b_start_dt
                        worked_mins -= int(b_diff.total_seconds() / 60)
                worked_mins = max(0, worked_mins)
                
            results.append({
                "id": first_in.id,
                "date": check_date,
                "check_in_at": first_in.check_time,
                "check_out_at": last_out.check_time if last_out else None,
                "location": first_in.location,
                "status": "checked_out" if last_out else "present",
                "worked_minutes": worked_mins,
                "notes": first_in.reason
            })
            
        return Response(results, status=status.HTTP_200_OK)



