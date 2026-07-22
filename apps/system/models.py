from django.db import models


# ---------------------------------------------------------------------------
# Status / Enum Choices
# ---------------------------------------------------------------------------

class UserStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    SUSPENDED = 'suspended', 'Suspended'


class CompanyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class DelegationStatus(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'


class LoginStatus(models.TextChoices):
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'


class LoginMethod(models.TextChoices):
    PASSWORD = 'password', 'Password'
    TWO_FA = '2fa', '2FA'
    SSO = 'sso', 'SSO'


# ---------------------------------------------------------------------------
# Role
# ---------------------------------------------------------------------------

class Role(models.Model):
    """
    User role with permissions.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=list, blank=True)
    user_count = models.IntegerField(default=0)
    is_system = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# System User
# ---------------------------------------------------------------------------

class SystemUser(models.Model):
    """
    System user for admin/management access.
    """
    user_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=500)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='users',
    )
    branch = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
    )
    two_fa = models.BooleanField(default=False)
    avatar_initials = models.CharField(max_length=10, blank=True, null=True)
    avatar_color = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'System User'
        verbose_name_plural = 'System Users'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Approval Workflow
# ---------------------------------------------------------------------------

class ApprovalWorkflow(models.Model):
    """
    Approval workflow configuration per module.
    """
    module = models.CharField(max_length=100)
    step_order = models.IntegerField()
    approver_role = models.CharField(max_length=100, blank=True, null=True)
    threshold = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    auto_approve_under = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    current_pending = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Approval Workflow'
        verbose_name_plural = 'Approval Workflows'
        ordering = ['module', 'step_order']

    def __str__(self):
        return f"{self.module} - Step {self.step_order}"


# ---------------------------------------------------------------------------
# Delegation
# ---------------------------------------------------------------------------

class Delegation(models.Model):
    """
    User delegation (assign tasks/responsibilities to another user).
    """
    from_user = models.ForeignKey(
        SystemUser,
        on_delete=models.CASCADE,
        related_name='delegations_from',
    )
    to_user = models.ForeignKey(
        SystemUser,
        on_delete=models.CASCADE,
        related_name='delegations_to',
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    scope = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=DelegationStatus.choices,
        default=DelegationStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Delegation'
        verbose_name_plural = 'Delegations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.name} -> {self.to_user.name}"


# ---------------------------------------------------------------------------
# Login Event
# ---------------------------------------------------------------------------

class LoginEvent(models.Model):
    """
    Login attempt log.
    """
    user = models.ForeignKey(
        SystemUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='login_events',
    )
    user_name = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=LoginStatus.choices,
    )
    method = models.CharField(
        max_length=50,
        choices=LoginMethod.choices,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Login Event'
        verbose_name_plural = 'Login Events'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user_name} - {self.status} - {self.timestamp}"


# ---------------------------------------------------------------------------
# Device Session
# ---------------------------------------------------------------------------

class DeviceSession(models.Model):
    """
    Active device session tracking.
    """
    user = models.ForeignKey(
        SystemUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='device_sessions',
    )
    user_name = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=DelegationStatus.choices,
        default=DelegationStatus.ACTIVE,
    )

    class Meta:
        verbose_name = 'Device Session'
        verbose_name_plural = 'Device Sessions'
        ordering = ['-last_active']

    def __str__(self):
        return f"{self.user_name} - {self.device}"
