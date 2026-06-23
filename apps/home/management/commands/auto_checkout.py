from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.home.models import AttendanceCheck
from apps.authapp.models import Employee
from datetime import datetime

class Command(BaseCommand):
    help = 'Automatically checks out employees who are still checked in at 10 PM'

    def handle(self, *args, **kwargs):
        # 1. Get current date/time info
        now = timezone.now()
        today_date_str = timezone.localdate().isoformat()
        
        # 2. Find all active employees
        employees = Employee.objects.filter(
            is_active=True,
            is_deleted=False, 
            is_superuser=False,
            is_staff=False
        )
        
        count = 0
        
        for employee in employees:
            # Check the LAST attendance record for today
            last_record = AttendanceCheck.objects.filter(
                employee=employee,
                check_date=today_date_str
            ).order_by('created_at').last()
            
            # If the last record is 'in', it means they are currently checked in (forgot to checkout)
            if last_record and last_record.check_type == 'in':
                # Create a force checkout record
                AttendanceCheck.objects.create(
                    employee=employee,
                    check_type='out',
                    check_date=today_date_str,
                    check_time="22:00:00", # Force to 10 PM
                    time_zone=last_record.time_zone, # Use same timezone as check-in
                    location="System Auto-Checkout",
                    reason="Auto-checkout (System) - Forgot to checkout"
                )
                
                self.stdout.write(self.style.SUCCESS(f'Auto-checked out: {employee.employee_name} ({employee.employeeId})'))
                count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully processed. Auto-checked out {count} employees.'))
