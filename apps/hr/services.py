from django.db import transaction
from typing import Dict, Any, List
from .models import Employee, AttendanceRecord, LeaveRequest, EmpDocument, EmpDocumentFile, EmpStatus, LeaveRequestStatus


# ===========================================================================
# EMPLOYEE SERVICES
# ===========================================================================

def get_all_employees() -> List[Employee]:
    return Employee.objects.all()

def create_employee(data: Dict[str, Any]) -> Employee:
    password = data.pop('password', None)
    employee = Employee(**data)
    if password:
        employee.set_password(password)
    else:
        employee.set_unusable_password()
    employee.save()
    return employee

def update_employee(employee: Employee, data: Dict[str, Any]) -> Employee:
    password = data.pop('password', None)
    for field, value in data.items():
        setattr(employee, field, value)
    if password:
        employee.set_password(password)
    employee.save()
    return employee

def deactivate_employee(employee: Employee) -> Employee:
    """Soft deletes the employee."""
    employee.status = EmpStatus.INACTIVE
    employee.is_active = False
    employee.save()
    return employee

def delete_employee(employee: Employee) -> None:
    """Hard deletes the employee from the database."""
    employee.delete()


# ===========================================================================
# ATTENDANCE SERVICES
# ===========================================================================

def get_all_attendance() -> List[AttendanceRecord]:
    return AttendanceRecord.objects.all()

def create_attendance(data: Dict[str, Any]) -> AttendanceRecord:
    return AttendanceRecord.objects.create(**data)

def update_attendance(attendance: AttendanceRecord, data: Dict[str, Any]) -> AttendanceRecord:
    for field, value in data.items():
        setattr(attendance, field, value)
    attendance.save()
    return attendance

def delete_attendance(attendance: AttendanceRecord) -> None:
    """Hard deletes the attendance record."""
    attendance.delete()


# ===========================================================================
# LEAVE REQUEST SERVICES
# ===========================================================================

def get_all_leave_requests() -> List[LeaveRequest]:
    return LeaveRequest.objects.all()

def create_leave_request(data: Dict[str, Any]) -> LeaveRequest:
    return LeaveRequest.objects.create(**data)

def update_leave_request(leave_request: LeaveRequest, data: Dict[str, Any]) -> LeaveRequest:
    for field, value in data.items():
        setattr(leave_request, field, value)
    leave_request.save()
    return leave_request

def approve_leave_request(leave_request: LeaveRequest, approved_by: str) -> LeaveRequest:
    """Approve a leave request."""
    leave_request.status = LeaveRequestStatus.APPROVED
    leave_request.approved_by = approved_by
    from django.utils import timezone
    leave_request.approved_at = timezone.now()
    leave_request.save()
    return leave_request

def reject_leave_request(leave_request: LeaveRequest, approved_by: str) -> LeaveRequest:
    """Reject a leave request."""
    leave_request.status = LeaveRequestStatus.REJECTED
    leave_request.approved_by = approved_by
    from django.utils import timezone
    leave_request.approved_at = timezone.now()
    leave_request.save()
    return leave_request

def delete_leave_request(leave_request: LeaveRequest) -> None:
    """Hard deletes the leave request."""
    leave_request.delete()


# ===========================================================================
# EMPLOYEE DOCUMENT SERVICES
# ===========================================================================

def get_all_documents() -> List[EmpDocument]:
    return EmpDocument.objects.all()

def create_document(data: Dict[str, Any]) -> EmpDocument:
    uploaded_files = data.pop('uploaded_files', [])
    with transaction.atomic():
        document = EmpDocument.objects.create(**data)
        for uploaded_file in uploaded_files:
            EmpDocumentFile.objects.create(
                document=document, file=uploaded_file, file_name=uploaded_file.name,
            )
    return document

def update_document(document: EmpDocument, data: Dict[str, Any]) -> EmpDocument:
    uploaded_files = data.pop('uploaded_files', [])
    with transaction.atomic():
        for field, value in data.items():
            setattr(document, field, value)
        document.save()
        for uploaded_file in uploaded_files:
            EmpDocumentFile.objects.create(
                document=document, file=uploaded_file, file_name=uploaded_file.name,
            )
    return document

def delete_document(document: EmpDocument) -> None:
    """Hard deletes the document."""
    document.delete()
