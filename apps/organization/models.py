from django.db import models


# ---------------------------------------------------------------------------
# Status / Enum Choices
# ---------------------------------------------------------------------------

class CompanyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

class Company(models.Model):
    """
    Top-level legal entity.  Mirrors the ``companies`` SQL table.
    """
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    initials = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    trn = models.CharField(max_length=50, blank=True, null=True, verbose_name='TRN')
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    established = models.IntegerField(blank=True, null=True, help_text='Year established')
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Branch
# ---------------------------------------------------------------------------

class Branch(models.Model):
    """
    A geographical / operational branch of a company.
    Mirrors the ``branches`` SQL table.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='branches',
    )
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    branch_head = models.CharField(max_length=255, blank=True, null=True)
    employee_count = models.IntegerField(default=0)
    dept_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.company.name})"


# ---------------------------------------------------------------------------
# Plant
# ---------------------------------------------------------------------------

class Plant(models.Model):
    """
    A physical plant / facility within a branch.
    Mirrors the ``plants`` SQL table.
    """

    PLANT_TYPE_CHOICES = [
        ('Manufacturing', 'Manufacturing'),
        ('Assembly', 'Assembly'),
        ('Warehouse', 'Warehouse'),
        ('QC', 'QC'),
    ]

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='plants',
    )
    # Denormalised snapshot of the branch name (as per original schema)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=PLANT_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Plant'
        verbose_name_plural = 'Plants'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-populate denormalised branch_name
        if self.branch_id and not self.branch_name:
            self.branch_name = self.branch.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Department
# ---------------------------------------------------------------------------

class Department(models.Model):
    """
    An organisational department, optionally linked to a branch.
    Mirrors the ``departments`` SQL table.
    """
    name = models.CharField(max_length=255)
    head = models.CharField(max_length=255, blank=True, null=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='departments',
    )
    # Denormalised snapshot
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    employee_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.branch_id and not self.branch_name:
            self.branch_name = self.branch.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Designation
# ---------------------------------------------------------------------------

class Designation(models.Model):
    """
    A job designation / role level within a department.
    Mirrors the ``designations`` SQL table.
    """

    LEVEL_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
        ('Lead', 'Lead'),
        ('Manager', 'Manager'),
        ('Director', 'Director'),
    ]

    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
    )
    grade = models.CharField(max_length=20, blank=True, null=True)
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'
        ordering = ['title']

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------------

class Team(models.Model):
    """
    A cross-functional or department-level team.
    Mirrors the ``teams`` SQL table.
    """
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    lead = models.CharField(max_length=255, blank=True, null=True)
    member_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------   
# Shift
# ---------------------------------------------------------------------------

class Shift(models.Model):
    """
    A work shift definition (time window + working days).
    Mirrors the ``shifts`` SQL table.
    """
    name = models.CharField(max_length=100)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    # Comma-separated day names, e.g. "Mon,Tue,Wed,Thu,Fri"
    days = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'
        ordering = ['name']

    def __str__(self):
        return self.name
