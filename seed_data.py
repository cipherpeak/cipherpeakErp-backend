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

print("Seeding database...")

# ===========================================================================
# ORGANIZATION
# ===========================================================================

print("\n[1/7] Creating Companies...")
c1 = Company.objects.create(name="Acme Corporation", legal_name="Acme Corporation Ltd", initials="AC", industry="Manufacturing", country="UAE", trn="100200300", phone="+971501234567", email="info@acme.com", address="Dubai, UAE", established=2015, status="active")
c2 = Company.objects.create(name="TechFlow Solutions", legal_name="TechFlow Solutions LLC", initials="TF", industry="Technology", country="UAE", trn="100200301", phone="+971509876543", email="info@techflow.com", address="Abu Dhabi, UAE", established=2018, status="active")
c3 = Company.objects.create(name="Gulf Industries", legal_name="Gulf Industries Group", initials="GI", industry="Industrial", country="SA", trn="300400500", phone="+966501234567", email="info@gulf.com", address="Riyadh, KSA", established=2010, status="active")
print(f"  Created {Company.objects.count()} companies")

print("\n[2/7] Creating Branches...")
b1 = Branch.objects.create(company=c1, name="Dubai Main Branch", city="Dubai", country="UAE", address="Sheikh Zayed Road", phone="+971501234567", email="dubai@acme.com", branch_head="Ahmed Ali", employee_count=50, dept_count=5, status="active")
b2 = Branch.objects.create(company=c1, name="Abu Dhabi Branch", city="Abu Dhabi", country="UAE", address="Corniche Road", phone="+971501234568", email="abudhabi@acme.com", branch_head="Sara Khan", employee_count=30, dept_count=4, status="active")
b3 = Branch.objects.create(company=c2, name="Dubai Tech Hub", city="Dubai", country="UAE", address="Internet City", phone="+971509876544", email="dubai@techflow.com", branch_head="Mike Johnson", employee_count=25, dept_count=3, status="active")
b4 = Branch.objects.create(company=c3, name="Riyadh Branch", city="Riyadh", country="SA", address="King Fahd Road", phone="+966501234568", email="riyadh@gulf.com", branch_head="Omar Hassan", employee_count=40, dept_count=4, status="active")
print(f"  Created {Branch.objects.count()} branches")

print("\n[3/7] Creating Plants...")
p1 = Plant.objects.create(branch=b1, name="Main Factory", type="Manufacturing", address="Industrial Area, Dubai", status="active")
p2 = Plant.objects.create(branch=b1, name="Assembly Unit", type="Assembly", address="Jebel Ali, Dubai", status="active")
p3 = Plant.objects.create(branch=b2, name="Warehouse A", type="Warehouse", address="Khalifa Port, Abu Dhabi", status="active")
print(f"  Created {Plant.objects.count()} plants")

print("\n[4/7] Creating Departments...")
d1 = Department.objects.create(name="Engineering", head="John Smith", branch=b1, employee_count=20, status="active")
d2 = Department.objects.create(name="Human Resources", head="Lisa Brown", branch=b1, employee_count=8, status="active")
d3 = Department.objects.create(name="Finance", head="David Lee", branch=b1, employee_count=6, status="active")
d4 = Department.objects.create(name="Operations", head="Sarah Wilson", branch=b2, employee_count=15, status="active")
d5 = Department.objects.create(name="IT", head="Mike Chen", branch=b3, employee_count=12, status="active")
print(f"  Created {Department.objects.count()} departments")

print("\n[5/7] Creating Designations, Teams, Shifts...")
des1 = Designation.objects.create(title="Software Engineer", department="Engineering", level="Mid", grade="B2", min_salary=8000, max_salary=15000, status="active")
des2 = Designation.objects.create(title="Senior Engineer", department="Engineering", level="Senior", grade="C1", min_salary=15000, max_salary=25000, status="active")
des3 = Designation.objects.create(title="HR Manager", department="Human Resources", level="Manager", grade="D1", min_salary=20000, max_salary=35000, status="active")
t1 = Team.objects.create(name="Backend Team", department="Engineering", lead="John Smith", member_count=8, status="active")
t2 = Team.objects.create(name="Frontend Team", department="Engineering", lead="Jane Doe", member_count=6, status="active")
s1 = Shift.objects.create(name="Morning Shift", start_time="09:00", end_time="17:00", days="Mon,Tue,Wed,Thu,Fri", status="active")
s2 = Shift.objects.create(name="Evening Shift", start_time="14:00", end_time="22:00", days="Mon,Tue,Wed,Thu,Fri", status="active")
print(f"  Created {Designation.objects.count()} designations, {Team.objects.count()} teams, {Shift.objects.count()} shifts")

# ===========================================================================
# HR
# ===========================================================================

print("\n[6/7] Creating Employees...")
emp1 = Employee.objects.create_superuser(emp_id="EMP001", password="password123", name="John Smith", email="john@acme.com", phone="+971501111111", avatar_initials="JS", avatar_color="#3B82F6", department="Engineering", designation="Senior Engineer", branch="Dubai Main Branch", shift="Morning", manager="Ahmed Ali", join_date="2020-01-15", nationality="British", gender="male", status="active", is_staff=True)
emp2 = Employee.objects.create_user(emp_id="EMP002", password="password123", name="Jane Doe", email="jane@acme.com", phone="+971502222222", avatar_initials="JD", avatar_color="#10B981", department="Engineering", designation="Software Engineer", branch="Dubai Main Branch", shift="Morning", manager="John Smith", join_date="2021-06-01", nationality="American", gender="female", status="active")
emp3 = Employee.objects.create_user(emp_id="EMP003", password="password123", name="Ahmed Ali", email="ahmed@acme.com", phone="+971503333333", avatar_initials="AA", avatar_color="#F59E0B", department="Operations", designation="Branch Manager", branch="Abu Dhabi Branch", shift="Morning", manager=None, join_date="2019-03-10", nationality="Emirati", gender="male", status="active")
emp4 = Employee.objects.create_user(emp_id="EMP004", password="password123", name="Sara Khan", email="sara@acme.com", phone="+971504444444", avatar_initials="SK", avatar_color="#EC4899", department="Human Resources", designation="HR Manager", branch="Dubai Main Branch", shift="Morning", manager="Ahmed Ali", join_date="2020-08-20", nationality="Pakistani", gender="female", status="active")
emp5 = Employee.objects.create_user(emp_id="EMP005", password="password123", name="David Lee", email="david@acme.com", phone="+971505555555", avatar_initials="DL", avatar_color="#8B5CF6", department="Finance", designation="Finance Manager", branch="Dubai Main Branch", shift="Morning", manager="Ahmed Ali", join_date="2021-02-15", nationality="Indian", gender="male", status="active")
emp6 = Employee.objects.create_user(emp_id="EMP006", password="password123", name="Lisa Brown", email="lisa@techflow.com", phone="+971506666666", avatar_initials="LB", avatar_color="#06B6D4", department="IT", designation="IT Manager", branch="Dubai Tech Hub", shift="Evening", manager="Mike Johnson", join_date="2022-01-10", nationality="Canadian", gender="female", status="active")
emp7 = Employee.objects.create_user(emp_id="EMP007", password="password123", name="Omar Hassan", email="omar@gulf.com", phone="+966507777777", avatar_initials="OH", avatar_color="#EF4444", department="Operations", designation="Operations Head", branch="Riyadh Branch", shift="Morning", manager=None, join_date="2018-05-01", nationality="Saudi", gender="male", status="active")
emp8 = Employee.objects.create_user(emp_id="EMP008", password="password123", name="Maria Garcia", email="maria@acme.com", phone="+971508888888", avatar_initials="MG", avatar_color="#14B8A6", department="Engineering", designation="Software Engineer", branch="Dubai Main Branch", shift="Evening", manager="John Smith", join_date="2023-03-01", nationality="Spanish", gender="female", status="active")
print(f"  Created {Employee.objects.count()} employees")

print("\n  Creating Attendance Records...")
today = date.today()
for i in range(7):
    d = today - timedelta(days=i)
    AttendanceRecord.objects.create(employee=emp1, date=d, check_in=timezone.make_aware(datetime(d.year, d.month, d.day, 9, 0)), check_out=timezone.make_aware(datetime(d.year, d.month, d.day, 17, 30)), status="present", hours_worked=8.5, overtime_hours=0.5, remarks="Regular day")
    AttendanceRecord.objects.create(employee=emp2, date=d, check_in=timezone.make_aware(datetime(d.year, d.month, d.day, 9, 15)), check_out=timezone.make_aware(datetime(d.year, d.month, d.day, 17, 0)), status="present", hours_worked=7.75, overtime_hours=0, remarks="Regular day")
    AttendanceRecord.objects.create(employee=emp3, date=d, check_in=timezone.make_aware(datetime(d.year, d.month, d.day, 8, 45)), check_out=timezone.make_aware(datetime(d.year, d.month, d.day, 18, 0)), status="present", hours_worked=9.25, overtime_hours=1.25, remarks="Extra work")
print(f"  Created {AttendanceRecord.objects.count()} attendance records")

print("\n  Creating Leave Requests...")
lr1 = LeaveRequest.objects.create(employee=emp1, type="annual", start_date=today + timedelta(days=10), end_date=today + timedelta(days=14), days=5.0, reason="Family vacation", status="pending")
lr2 = LeaveRequest.objects.create(employee=emp2, type="sick", start_date=today - timedelta(days=3), end_date=today - timedelta(days=2), days=2.0, reason="Doctor appointment", status="approved", approved_by="John Smith", approved_at=timezone.now())
lr3 = LeaveRequest.objects.create(employee=emp4, type="casual", start_date=today + timedelta(days=5), end_date=today + timedelta(days=5), days=1.0, reason="Personal work", status="pending")
lr4 = LeaveRequest.objects.create(employee=emp5, type="annual", start_date=today + timedelta(days=20), end_date=today + timedelta(days=25), days=6.0, reason="Holiday trip", status="rejected", approved_by="Ahmed Ali", approved_at=timezone.now())
print(f"  Created {LeaveRequest.objects.count()} leave requests")

print("\n  Creating Employee Documents...")
doc1 = EmpDocument.objects.create(employee=emp1, type="visa", document_number="V98765432", issue_date="2023-01-01", expiry_date="2025-01-01", file_name="visa_js.pdf", status="valid")
doc2 = EmpDocument.objects.create(employee=emp1, type="contract", document_number="CTR001", issue_date="2023-01-15", expiry_date="2025-01-15", file_name="contract_js.pdf", status="valid")
doc3 = EmpDocument.objects.create(employee=emp3, type="emirates_id", document_number="EID7890123", issue_date="2022-06-01", expiry_date="2024-06-01", file_name="eid_aa.pdf", status="expiring")
doc4 = EmpDocument.objects.create(employee=emp4, type="visa", document_number="V12345678", issue_date="2023-06-01", expiry_date="2025-06-01", file_name="visa_sk.pdf", status="valid")
print(f"  Created {EmpDocument.objects.count()} documents")

# ===========================================================================
# SYSTEM
# ===========================================================================

print("\n[7/7] Creating System Data...")
r1 = Role.objects.create(name="Super Admin", description="Full system access", permissions=["read", "write", "delete", "approve", "manage_users"], user_count=1, is_system=True)
r2 = Role.objects.create(name="Admin", description="Admin access", permissions=["read", "write", "delete", "approve"], user_count=2, is_system=True)
r3 = Role.objects.create(name="Manager", description="Manager access", permissions=["read", "write", "approve"], user_count=3, is_system=False)
r4 = Role.objects.create(name="Employee", description="Basic employee access", permissions=["read"], user_count=5, is_system=False)
print(f"  Created {Role.objects.count()} roles")

su1 = SystemUser.objects.create(name="Super Admin", email="superadmin@acme.com", password_hash=make_password("admin123"), role=r1, branch="Dubai Main Branch", department="IT", status="active", two_fa=False, avatar_initials="SA", avatar_color="#EF4444")
su2 = SystemUser.objects.create(name="HR Admin", email="hradmin@acme.com", password_hash=make_password("admin123"), role=r2, branch="Dubai Main Branch", department="Human Resources", status="active", two_fa=True, avatar_initials="HA", avatar_color="#3B82F6")
su3 = SystemUser.objects.create(name="Branch Manager", email="branchmgr@acme.com", password_hash=make_password("admin123"), role=r3, branch="Abu Dhabi Branch", department="Operations", status="active", two_fa=False, avatar_initials="BM", avatar_color="#10B981")
print(f"  Created {SystemUser.objects.count()} system users")

aw1 = ApprovalWorkflow.objects.create(module="leave_request", step_order=1, approver_role="Manager", threshold=5000.00, auto_approve_under=100.00, status="active", current_pending=2)
aw2 = ApprovalWorkflow.objects.create(module="leave_request", step_order=2, approver_role="HR Manager", threshold=10000.00, auto_approve_under=None, status="active", current_pending=1)
aw3 = ApprovalWorkflow.objects.create(module="purchase_order", step_order=1, approver_role="Manager", threshold=25000.00, auto_approve_under=500.00, status="active", current_pending=0)
print(f"  Created {ApprovalWorkflow.objects.count()} workflows")

del1 = Delegation.objects.create(from_user=su1, to_user=su2, start_date=date.today(), end_date=date.today() + timedelta(days=14), reason="Vacation coverage", status="active")
del2 = Delegation.objects.create(from_user=su3, to_user=su1, start_date=date.today() - timedelta(days=5), end_date=date.today() + timedelta(days=5), reason="Project handover", status="active")
print(f"  Created {Delegation.objects.count()} delegations")

le1 = LoginEvent.objects.create(user=su1, user_name="Super Admin", ip="192.168.1.100", device="Windows PC", location="Dubai, UAE", status="success", method="password")
le2 = LoginEvent.objects.create(user=su2, user_name="HR Admin", ip="192.168.1.101", device="MacBook Pro", location="Dubai, UAE", status="success", method="2fa")
le3 = LoginEvent.objects.create(user=None, user_name="Unknown", ip="10.0.0.50", device="Unknown", location="Unknown", status="failed", method="password")
print(f"  Created {LoginEvent.objects.count()} login events")

ds1 = DeviceSession.objects.create(user=su1, user_name="Super Admin", device="Windows PC", browser="Chrome 125", ip="192.168.1.100", location="Dubai, UAE", last_active=timezone.now(), status="active")
ds2 = DeviceSession.objects.create(user=su2, user_name="HR Admin", device="MacBook Pro", browser="Safari 17", ip="192.168.1.101", location="Dubai, UAE", last_active=timezone.now() - timedelta(hours=2), status="active")
ds3 = DeviceSession.objects.create(user=su3, user_name="Branch Manager", device="iPhone 15", browser="Safari Mobile", ip="192.168.2.50", location="Abu Dhabi, UAE", last_active=timezone.now() - timedelta(days=1), status="expired")
print(f"  Created {DeviceSession.objects.count()} device sessions")

print("\n" + "="*50)
print("DATABASE SEEDED SUCCESSFULLY!")
print("="*50)
print(f"\nOrganizations: {Company.objects.count()} companies, {Branch.objects.count()} branches, {Plant.objects.count()} plants, {Department.objects.count()} departments")
print(f"HR: {Employee.objects.count()} employees, {AttendanceRecord.objects.count()} attendance records, {LeaveRequest.objects.count()} leave requests, {EmpDocument.objects.count()} documents")
print(f"System: {Role.objects.count()} roles, {SystemUser.objects.count()} users, {ApprovalWorkflow.objects.count()} workflows, {Delegation.objects.count()} delegations")
print(f"\nLogin credentials:")
print(f"  Employee Login:  emp_id=EMP001, password=password123")
print(f"  Admin Login:     emp_id=EMP001, password=password123 (is_staff=True)")
