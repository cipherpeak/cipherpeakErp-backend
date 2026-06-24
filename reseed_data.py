import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.organization.models import Company, Branch, Plant, Department, Designation, Team, Shift
from apps.hr.models import Employee, AttendanceRecord, LeaveRequest, EmpDocument
from apps.system.models import Role, SystemUser, ApprovalWorkflow, Delegation, LoginEvent, DeviceSession
from django.contrib.auth.hashers import make_password
from datetime import date, datetime, timedelta
from django.utils import timezone

print("Seeding database with FK relationships...")

# Get existing org data
c1 = Company.objects.get(name="Acme Corporation")
c2 = Company.objects.get(name="TechFlow Solutions")
c3 = Company.objects.get(name="Gulf Industries")
b1 = Branch.objects.get(name="Dubai Main Branch")
b2 = Branch.objects.get(name="Abu Dhabi Branch")
b3 = Branch.objects.get(name="Dubai Tech Hub")
b4 = Branch.objects.get(name="Riyadh Branch")
d1 = Department.objects.get(name="Engineering")
d2 = Department.objects.get(name="Human Resources")
d3 = Department.objects.get(name="Finance")
d4 = Department.objects.get(name="Operations")
d5 = Department.objects.get(name="IT")

print("\nCreating Employees with FK relationships...")
emp1 = Employee.objects.create_superuser(emp_id="EMP001", password="password123", name="John Smith", email="john@acme.com", phone="+971501111111", avatar_initials="JS", avatar_color="#3B82F6", department=d1, designation="Senior Engineer", branch=b1, shift="Morning", manager="Ahmed Ali", join_date="2020-01-15", nationality="British", gender="male", status="active", is_staff=True)
emp2 = Employee.objects.create_user(emp_id="EMP002", password="password123", name="Jane Doe", email="jane@acme.com", phone="+971502222222", avatar_initials="JD", avatar_color="#10B981", department=d1, designation="Software Engineer", branch=b1, shift="Morning", manager="John Smith", join_date="2021-06-01", nationality="American", gender="female", status="active")
emp3 = Employee.objects.create_user(emp_id="EMP003", password="password123", name="Ahmed Ali", email="ahmed@acme.com", phone="+971503333333", avatar_initials="AA", avatar_color="#F59E0B", department=d4, designation="Branch Manager", branch=b2, shift="Morning", manager=None, join_date="2019-03-10", nationality="Emirati", gender="male", status="active")
emp4 = Employee.objects.create_user(emp_id="EMP004", password="password123", name="Sara Khan", email="sara@acme.com", phone="+971504444444", avatar_initials="SK", avatar_color="#EC4899", department=d2, designation="HR Manager", branch=b1, shift="Morning", manager="Ahmed Ali", join_date="2020-08-20", nationality="Pakistani", gender="female", status="active")
emp5 = Employee.objects.create_user(emp_id="EMP005", password="password123", name="David Lee", email="david@acme.com", phone="+971505555555", avatar_initials="DL", avatar_color="#8B5CF6", department=d3, designation="Finance Manager", branch=b1, shift="Morning", manager="Ahmed Ali", join_date="2021-02-15", nationality="Indian", gender="male", status="active")
emp6 = Employee.objects.create_user(emp_id="EMP006", password="password123", name="Lisa Brown", email="lisa@techflow.com", phone="+971506666666", avatar_initials="LB", avatar_color="#06B6D4", department=d5, designation="IT Manager", branch=b3, shift="Evening", manager="Mike Johnson", join_date="2022-01-10", nationality="Canadian", gender="female", status="active")
emp7 = Employee.objects.create_user(emp_id="EMP007", password="password123", name="Omar Hassan", email="omar@gulf.com", phone="+966507777777", avatar_initials="OH", avatar_color="#EF4444", department=d4, designation="Operations Head", branch=b4, shift="Morning", manager=None, join_date="2018-05-01", nationality="Saudi", gender="male", status="active")
emp8 = Employee.objects.create_user(emp_id="EMP008", password="password123", name="Maria Garcia", email="maria@acme.com", phone="+971508888888", avatar_initials="MG", avatar_color="#14B8A6", department=d1, designation="Software Engineer", branch=b1, shift="Evening", manager="John Smith", join_date="2023-03-01", nationality="Spanish", gender="female", status="active")
emp9 = Employee.objects.create_user(emp_id="EMP009", password="password123", name="Tom Wilson", email="tom@acme.com", phone="+971509999999", avatar_initials="TW", avatar_color="#F97316", department=d1, designation="Junior Developer", branch=b1, shift="Morning", manager="John Smith", join_date="2024-01-15", nationality="Australian", gender="male", status="active")
emp10 = Employee.objects.create_user(emp_id="EMP010", password="password123", name="Fatima Al-Rashid", email="fatima@acme.com", phone="+971500000000", avatar_initials="FA", avatar_color="#A855F7", department=d2, designation="HR Specialist", branch=b2, shift="Morning", manager="Sara Khan", join_date="2023-09-01", nationality="Emirati", gender="female", status="active")
print(f"  Created {Employee.objects.count()} employees")

print("\nCreating Attendance Records...")
today = date.today()
for i in range(7):
    d = today - timedelta(days=i)
    AttendanceRecord.objects.create(employee=emp1, date=d, check_in=timezone.make_aware(datetime(d.year, d.month, d.day, 9, 0)), check_out=timezone.make_aware(datetime(d.year, d.month, d.day, 17, 30)), status="present", hours_worked=8.5, overtime_hours=0.5, remarks="Regular day")
    AttendanceRecord.objects.create(employee=emp2, date=d, check_in=timezone.make_aware(datetime(d.year, d.month, d.day, 9, 15)), check_out=timezone.make_aware(datetime(d.year, d.month, d.day, 17, 0)), status="present", hours_worked=7.75, overtime_hours=0, remarks="Regular day")
    AttendanceRecord.objects.create(employee=emp3, date=d, check_in=timezone.make_aware(datetime(d.year, d.month, d.day, 8, 45)), check_out=timezone.make_aware(datetime(d.year, d.month, d.day, 18, 0)), status="present", hours_worked=9.25, overtime_hours=1.25, remarks="Extra work")
print(f"  Created {AttendanceRecord.objects.count()} attendance records")

print("\nCreating Leave Requests...")
lr1 = LeaveRequest.objects.create(employee=emp1, type="annual", start_date=today + timedelta(days=10), end_date=today + timedelta(days=14), days=5.0, reason="Family vacation", status="pending")
lr2 = LeaveRequest.objects.create(employee=emp2, type="sick", start_date=today - timedelta(days=3), end_date=today - timedelta(days=2), days=2.0, reason="Doctor appointment", status="approved", approved_by="John Smith", approved_at=timezone.now())
lr3 = LeaveRequest.objects.create(employee=emp4, type="casual", start_date=today + timedelta(days=5), end_date=today + timedelta(days=5), days=1.0, reason="Personal work", status="pending")
lr4 = LeaveRequest.objects.create(employee=emp5, type="annual", start_date=today + timedelta(days=20), end_date=today + timedelta(days=25), days=6.0, reason="Holiday trip", status="rejected", approved_by="Ahmed Ali", approved_at=timezone.now())
print(f"  Created {LeaveRequest.objects.count()} leave requests")

print("\nCreating Employee Documents...")
doc1 = EmpDocument.objects.create(employee=emp1, type="visa", document_number="V98765432", issue_date="2023-01-01", expiry_date="2025-01-01", file_name="visa_js.pdf", status="valid")
doc2 = EmpDocument.objects.create(employee=emp1, type="contract", document_number="CTR001", issue_date="2023-01-15", expiry_date="2025-01-15", file_name="contract_js.pdf", status="valid")
doc3 = EmpDocument.objects.create(employee=emp3, type="emirates_id", document_number="EID7890123", issue_date="2022-06-01", expiry_date="2024-06-01", file_name="eid_aa.pdf", status="expiring")
doc4 = EmpDocument.objects.create(employee=emp4, type="visa", document_number="V12345678", issue_date="2023-06-01", expiry_date="2025-06-01", file_name="visa_sk.pdf", status="valid")
print(f"  Created {EmpDocument.objects.count()} documents")

print("\n" + "="*50)
print("DATABASE RE-SEEDED SUCCESSFULLY!")
print("="*50)
print(f"\nEmployees now have FK links:")
for emp in Employee.objects.select_related('department', 'branch').all():
    dept = emp.department.name if emp.department else "None"
    branch = emp.branch.name if emp.branch else "None"
    print(f"  {emp.emp_id} {emp.name} -> Dept: {dept}, Branch: {branch}")
