from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from typing import Dict, Any, List
from .models import Role, SystemUser, ApprovalWorkflow, Delegation, LoginEvent, DeviceSession, UserStatus, DelegationStatus


# ===========================================================================
# ROLE SERVICES
# ===========================================================================

def get_all_roles() -> List[Role]:
    return Role.objects.all()

def create_role(data: Dict[str, Any]) -> Role:
    return Role.objects.create(**data)

def update_role(role: Role, data: Dict[str, Any]) -> Role:
    for field, value in data.items():
        setattr(role, field, value)
    role.save()
    return role

def delete_role(role: Role) -> None:
    role.delete()


# ===========================================================================
# SYSTEM USER SERVICES
# ===========================================================================

def get_all_system_users() -> List[SystemUser]:
    return SystemUser.objects.all()

def create_system_user(data: Dict[str, Any]) -> SystemUser:
    password = data.pop('password_hash', None)
    user = SystemUser(**data)
    if not password:
        password = 'TempPassword123!'
    user.password_hash = make_password(password)
    user.save()
    return user

def update_system_user(user: SystemUser, data: Dict[str, Any]) -> SystemUser:
    password = data.pop('password_hash', None)
    for field, value in data.items():
        setattr(user, field, value)
    if password:
        user.password_hash = make_password(password)
    user.save()
    return user

def deactivate_system_user(user: SystemUser) -> SystemUser:
    user.status = UserStatus.INACTIVE
    user.save()
    return user

def delete_system_user(user: SystemUser) -> None:
    user.delete()

def authenticate_system_user(email: str, password: str) -> SystemUser:
    """Authenticate a system user by email and password."""
    try:
        user = SystemUser.objects.get(email=email)
    except SystemUser.DoesNotExist:
        return None
    
    if check_password(password, user.password_hash):
        from django.utils import timezone
        user.last_login = timezone.now()
        user.save()
        return user
    return None


# ===========================================================================
# APPROVAL WORKFLOW SERVICES
# ===========================================================================

def get_all_workflows() -> List[ApprovalWorkflow]:
    return ApprovalWorkflow.objects.all()

def create_workflow(data: Dict[str, Any]) -> ApprovalWorkflow:
    return ApprovalWorkflow.objects.create(**data)

def update_workflow(workflow: ApprovalWorkflow, data: Dict[str, Any]) -> ApprovalWorkflow:
    for field, value in data.items():
        setattr(workflow, field, value)
    workflow.save()
    return workflow

def delete_workflow(workflow: ApprovalWorkflow) -> None:
    workflow.delete()


# ===========================================================================
# DELEGATION SERVICES
# ===========================================================================

def get_all_delegations() -> List[Delegation]:
    return Delegation.objects.all()

def create_delegation(data: Dict[str, Any]) -> Delegation:
    return Delegation.objects.create(**data)

def update_delegation(delegation: Delegation, data: Dict[str, Any]) -> Delegation:
    for field, value in data.items():
        setattr(delegation, field, value)
    delegation.save()
    return delegation

def expire_delegation(delegation: Delegation) -> Delegation:
    delegation.status = DelegationStatus.EXPIRED
    delegation.save()
    return delegation

def delete_delegation(delegation: Delegation) -> None:
    delegation.delete()


# ===========================================================================
# LOGIN EVENT SERVICES
# ===========================================================================

def get_all_login_events() -> List[LoginEvent]:
    return LoginEvent.objects.all()

def create_login_event(data: Dict[str, Any]) -> LoginEvent:
    return LoginEvent.objects.create(**data)

def delete_login_event(event: LoginEvent) -> None:
    event.delete()


# ===========================================================================
# DEVICE SESSION SERVICES
# ===========================================================================

def get_all_device_sessions() -> List[DeviceSession]:
    return DeviceSession.objects.all()

def create_device_session(data: Dict[str, Any]) -> DeviceSession:
    return DeviceSession.objects.create(**data)

def update_device_session(session: DeviceSession, data: Dict[str, Any]) -> DeviceSession:
    for field, value in data.items():
        setattr(session, field, value)
    session.save()
    return session

def expire_device_session(session: DeviceSession) -> DeviceSession:
    session.status = DelegationStatus.EXPIRED
    session.save()
    return session

def delete_device_session(session: DeviceSession) -> None:
    session.delete()
