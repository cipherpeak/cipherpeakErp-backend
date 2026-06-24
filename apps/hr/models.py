from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ---------------------------------------------------------------------------
# Status / Enum Choices
# ---------------------------------------------------------------------------

class EmpStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    ON_LEAVE = 'on_leave', 'On Leave'
    TERMINATED = 'terminated', 'Terminated'


class AttendanceStatus(models.TextChoices):
    PRESENT = 'present', 'Present'
    ABSENT = 'absent', 'Absent'
    LATE = 'late', 'Late'
    HALF_DAY = 'half_day', 'Half Day'


class LeaveType(models.TextChoices):
    ANNUAL = 'annual', 'Annual'
    SICK = 'sick', 'Sick'
    CASUAL = 'casual', 'Casual'
    UNPAID = 'unpaid', 'Unpaid'


class LeaveRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


class DocumentType(models.TextChoices):
    VISA = 'visa', 'Visa'
    EMIRATES_ID = 'emirates_id', 'Emirates ID'
    TRADE_LICENSE = 'trade_license', 'Trade License'
    CONTRACT = 'contract', 'Contract'


class DocumentStatus(models.TextChoices):
    VALID = 'valid', 'Valid'
    EXPIRING = 'expiring', 'Expiring'
    EXPIRED = 'expired', 'Expired'


# ---------------------------------------------------------------------------
# Custom User Manager
# ---------------------------------------------------------------------------

class EmployeeManager(BaseUserManager):
    def create_user(self, emp_id, password=None, **extra_fields):
        if not emp_id:
            raise ValueError('Employee ID is required')
        user = self.model(emp_id=emp_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, emp_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(emp_id, password, **extra_fields)


# ---------------------------------------------------------------------------
# Employee (Custom User Model)
# ---------------------------------------------------------------------------

class Employee(AbstractBaseUser, PermissionsMixin):
    """
    Core employee record - serves as the custom user model.
    """
    emp_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    avatar_initials = models.CharField(max_length=10, blank=True, null=True)
    avatar_color = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    shift = models.CharField(max_length=100, blank=True, null=True)
    manager = models.CharField(max_length=255, blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=EmpStatus.choices,
        default=EmpStatus.ACTIVE,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'emp_id'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.emp_id})"


# ---------------------------------------------------------------------------
# Attendance Record
# ---------------------------------------------------------------------------

class AttendanceRecord(models.Model):
    """
    Daily attendance record for an employee.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    date = models.DateField()
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
    )
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        ordering = ['-date']
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.name} - {self.date}"


# ---------------------------------------------------------------------------
# Leave Request
# ---------------------------------------------------------------------------

class LeaveRequest(models.Model):
    """
    Employee leave request.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_requests',
    )
    type = models.CharField(
        max_length=20,
        choices=LeaveType.choices,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.DecimalField(max_digits=5, decimal_places=1)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=LeaveRequestStatus.choices,
        default=LeaveRequestStatus.PENDING,
    )
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.name} - {self.type} ({self.start_date} to {self.end_date})"


# ---------------------------------------------------------------------------
# Employee Document
# ---------------------------------------------------------------------------

class EmpDocument(models.Model):
    """
    Employee documents (visa, emirates ID, trade license, contract).
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
    )
    document_number = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.VALID,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Employee Document'
        verbose_name_plural = 'Employee Documents'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.name} - {self.type}"
