from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CurrencyCode(models.TextChoices):
    AED = 'AED', 'AED'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    INR = 'INR', 'INR'
    SAR = 'SAR', 'SAR'


class GenderType(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'


class JobStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ON_HOLD = 'on_hold', 'On Hold'
    CLOSED = 'closed', 'Closed'


class EmploymentType(models.TextChoices):
    FULL_TIME = 'full_time', 'Full Time'
    PART_TIME = 'part_time', 'Part Time'
    CONTRACT = 'contract', 'Contract'
    INTERNSHIP = 'internship', 'Internship'


class ApplicantStatus(models.TextChoices):
    APPLIED = 'applied', 'Applied'
    SCREENING = 'screening', 'Screening'
    INTERVIEW = 'interview', 'Interview'
    TECHNICAL = 'technical', 'Technical'
    HR_ROUND = 'hr_round', 'HR Round'
    OFFER_SENT = 'offer_sent', 'Offer Sent'
    HIRED = 'hired', 'Hired'
    REJECTED = 'rejected', 'Rejected'


class ApplicationSource(models.TextChoices):
    LINKEDIN = 'linkedin', 'LinkedIn'
    REFERRAL = 'referral', 'Referral'
    JOB_PORTAL = 'job_portal', 'Job Portal'
    WEBSITE = 'website', 'Website'
    WALK_IN = 'walk_in', 'Walk In'
    AGENCY = 'agency', 'Agency'


class InterviewStatus(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    RESCHEDULED = 'rescheduled', 'Rescheduled'
    NO_SHOW = 'no_show', 'No Show'


class InterviewMode(models.TextChoices):
    IN_PERSON = 'in_person', 'In Person'
    VIDEO_CALL = 'video_call', 'Video Call'
    PHONE = 'phone', 'Phone'
    PANEL = 'panel', 'Panel'


class OnboardingStatus(models.TextChoices):
    NOT_STARTED = 'not_started', 'Not Started'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    ON_HOLD = 'on_hold', 'On Hold'


class ExitType(models.TextChoices):
    RESIGNATION = 'resignation', 'Resignation'
    TERMINATION = 'termination', 'Termination'
    RETIREMENT = 'retirement', 'Retirement'
    CONTRACT_END = 'contract_end', 'Contract End'
    MUTUAL_SEPARATION = 'mutual_separation', 'Mutual Separation'


class ExitStatus(models.TextChoices):
    INITIATED = 'initiated', 'Initiated'
    CLEARANCE_IN_PROGRESS = 'clearance_in_progress', 'Clearance In Progress'
    CLEARANCE_COMPLETED = 'clearance_completed', 'Clearance Completed'
    SETTLEMENT_PROCESSED = 'settlement_processed', 'Settlement Processed'
    CLOSED = 'closed', 'Closed'


class ClearanceStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CLEARED = 'cleared', 'Cleared'
    NOT_APPLICABLE = 'not_applicable', 'Not Applicable'


class TrainingStatus(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class TrainingMode(models.TextChoices):
    CLASSROOM = 'classroom', 'Classroom'
    ONLINE = 'online', 'Online'
    ON_THE_JOB = 'on_the_job', 'On The Job'
    BLENDED = 'blended', 'Blended'
    EXTERNAL = 'external', 'External'


class EnrollmentStatus(models.TextChoices):
    ENROLLED = 'enrolled', 'Enrolled'
    COMPLETED = 'completed', 'Completed'
    WITHDREW = 'withdrew', 'Withdrew'
    FAILED = 'failed', 'Failed'


class ReviewStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    IN_PROGRESS = 'in_progress', 'In Progress'
    SUBMITTED = 'submitted', 'Submitted'
    ACKNOWLEDGED = 'acknowledged', 'Acknowledged'
    COMPLETED = 'completed', 'Completed'


class ReviewType(models.TextChoices):
    ANNUAL = 'annual', 'Annual'
    QUARTERLY = 'quarterly', 'Quarterly'
    PROBATION = 'probation', 'Probation'
    THREE_SIXTY = '360', '360'


class TravelStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class ClaimStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Submitted'
    UNDER_REVIEW = 'under_review', 'Under Review'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    PAID = 'paid', 'Paid'


class EmpAssetStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    ASSIGNED = 'assigned', 'Assigned'
    UNDER_REPAIR = 'under_repair', 'Under Repair'
    DISPOSED = 'disposed', 'Disposed'
    LOST = 'lost', 'Lost'


# ---------------------------------------------------------------------------
# Job Opening
# ---------------------------------------------------------------------------

class JobOpening(models.Model):
    job_code = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    department = models.ForeignKey(
        'organization.Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='job_openings',
    )
    department_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, blank=True, null=True)
    experience_min = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    experience_max = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    posted_date = models.DateField(blank=True, null=True)
    closing_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.DRAFT)
    description = models.TextField(blank=True, null=True)
    requirements = models.JSONField(default=list, blank=True)
    responsibilities = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Job Opening'
        verbose_name_plural = 'Job Openings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job_code} - {self.title}"

    def save(self, *args, **kwargs):
        if self.department and not self.department_name:
            self.department_name = self.department.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Applicant
# ---------------------------------------------------------------------------

class Applicant(models.Model):
    applicant_number = models.CharField(max_length=40, unique=True)
    job_opening = models.ForeignKey(
        JobOpening, on_delete=models.SET_NULL, blank=True, null=True, related_name='applicants',
    )
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    nationality = models.CharField(max_length=80, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GenderType.choices, blank=True, null=True)
    current_company = models.CharField(max_length=200, blank=True, null=True)
    current_role = models.CharField(max_length=150, blank=True, null=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    notice_period = models.CharField(max_length=40, blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    current_salary = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    source = models.CharField(max_length=20, choices=ApplicationSource.choices, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ApplicantStatus.choices, default=ApplicantStatus.APPLIED)
    applied_date = models.DateField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    rating = models.SmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant_number} - {self.name}"


# ---------------------------------------------------------------------------
# Interview
# ---------------------------------------------------------------------------

class Interview(models.Model):
    interview_number = models.CharField(max_length=40, unique=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='interviews')
    job_opening = models.ForeignKey(
        JobOpening, on_delete=models.SET_NULL, blank=True, null=True, related_name='interviews',
    )
    round = models.CharField(max_length=60, blank=True, null=True)
    interviewers = models.JSONField(default=list, blank=True)
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)
    duration_mins = models.IntegerField(blank=True, null=True)
    mode = models.CharField(max_length=20, choices=InterviewMode.choices, blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=InterviewStatus.choices, default=InterviewStatus.SCHEDULED)
    overall_rating = models.SmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    recommendation = models.CharField(max_length=30, blank=True, null=True, help_text='hire/reject/on_hold/next_round')
    feedback = models.TextField(blank=True, null=True)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'
        ordering = ['-created_at']

    def __str__(self):
        return self.interview_number


# ---------------------------------------------------------------------------
# Onboarding
# ---------------------------------------------------------------------------

class OnboardingRecord(models.Model):
    onboarding_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='onboarding_records',
    )
    join_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=OnboardingStatus.choices, default=OnboardingStatus.NOT_STARTED)
    buddy = models.CharField(max_length=150, blank=True, null=True)
    manager = models.CharField(max_length=150, blank=True, null=True)
    documents_pending = models.JSONField(default=list, blank=True)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Onboarding Record'
        verbose_name_plural = 'Onboarding Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.onboarding_number


class OnboardingTask(models.Model):
    onboarding = models.ForeignKey(OnboardingRecord, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=200)
    category = models.CharField(max_length=80, blank=True, null=True)
    responsible = models.CharField(max_length=150, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Onboarding Task'
        verbose_name_plural = 'Onboarding Tasks'

    def __str__(self):
        return f"{self.onboarding.onboarding_number} - {self.task}"


# ---------------------------------------------------------------------------
# Exit Management
# ---------------------------------------------------------------------------

class ExitRecord(models.Model):
    exit_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='exit_records',
    )
    exit_type = models.CharField(max_length=30, choices=ExitType.choices)
    status = models.CharField(max_length=30, choices=ExitStatus.choices, default=ExitStatus.INITIATED)
    last_working_day = models.DateField(blank=True, null=True)
    notice_period_served = models.IntegerField(blank=True, null=True)
    notice_period_required = models.IntegerField(blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    eos_gratuity = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    leave_encashment = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    pending_salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notice_recovery = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    travel_ticket = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_payable = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Exit Record'
        verbose_name_plural = 'Exit Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.exit_number


class ExitClearanceItem(models.Model):
    exit_record = models.ForeignKey(ExitRecord, on_delete=models.CASCADE, related_name='clearance_items')
    department = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=200)
    responsible_person = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ClearanceStatus.choices, default=ClearanceStatus.PENDING)
    cleared_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Exit Clearance Item'
        verbose_name_plural = 'Exit Clearance Items'

    def __str__(self):
        return f"{self.exit_record.exit_number} - {self.item}"


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

class TrainingProgram(models.Model):
    program_code = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    trainer = models.CharField(max_length=150, blank=True, null=True)
    trainer_organization = models.CharField(max_length=200, blank=True, null=True)
    mode = models.CharField(max_length=20, choices=TrainingMode.choices, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    duration_hours = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    enrolled = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=TrainingStatus.choices, default=TrainingStatus.UPCOMING)
    cost_per_participant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    certification = models.BooleanField(default=False)
    certification_name = models.CharField(max_length=200, blank=True, null=True)
    departments = models.JSONField(default=list, blank=True)
    skills_covered = models.JSONField(default=list, blank=True)
    pass_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Training Program'
        verbose_name_plural = 'Training Programs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.program_code} - {self.title}"


class TrainingEnrollment(models.Model):
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='enrollments')
    employee = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='training_enrollments',
    )
    enrollment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=EnrollmentStatus.choices, default=EnrollmentStatus.ENROLLED)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    certificate_issued = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Training Enrollment'
        verbose_name_plural = 'Training Enrollments'

    def __str__(self):
        return f"{self.program.program_code} - {self.employee}"


# ---------------------------------------------------------------------------
# Performance Review
# ---------------------------------------------------------------------------

class PerformanceReview(models.Model):
    review_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='performance_reviews')
    manager = models.CharField(max_length=150, blank=True, null=True)
    review_period = models.CharField(max_length=60, blank=True, null=True)
    review_type = models.CharField(max_length=20, choices=ReviewType.choices)
    status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.DRAFT)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return self.review_number


class ReviewKPI(models.Model):
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name='kpis')
    name = models.CharField(max_length=200)
    target = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    achieved = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=40, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Review KPI'
        verbose_name_plural = 'Review KPIs'

    def __str__(self):
        return f"{self.review.review_number} - {self.name}"


class ReviewGoal(models.Model):
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name='goals')
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True, help_text='pending/in_progress/completed/missed')
    completion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Review Goal'
        verbose_name_plural = 'Review Goals'

    def __str__(self):
        return f"{self.review.review_number} - goal"


class ReviewCompetency(models.Model):
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name='competencies')
    name = models.CharField(max_length=150)
    rating = models.SmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Review Competency'
        verbose_name_plural = 'Review Competencies'

    def __str__(self):
        return f"{self.review.review_number} - {self.name}"


# ---------------------------------------------------------------------------
# Travel Request
# ---------------------------------------------------------------------------

class TravelRequest(models.Model):
    request_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='travel_requests')
    destination_city = models.CharField(max_length=120, blank=True, null=True)
    destination_country = models.CharField(max_length=120, blank=True, null=True)
    purpose = models.CharField(max_length=60, blank=True, null=True)
    purpose_details = models.TextField(blank=True, null=True)
    travel_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    travel_days = models.IntegerField(blank=True, null=True)
    travel_mode = models.CharField(max_length=20, blank=True, null=True, help_text='air/road/rail/sea')
    travel_class = models.CharField(max_length=20, blank=True, null=True, help_text='economy/business')
    hotel_required = models.BooleanField(default=False)
    hotel_nights = models.IntegerField(default=0)
    estimated_ticket_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estimated_hotel_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estimated_per_diem = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estimated_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    advance_requested = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=TravelStatus.choices, default=TravelStatus.DRAFT)
    approver = models.CharField(max_length=150, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Travel Request'
        verbose_name_plural = 'Travel Requests'
        ordering = ['-created_at']

    def __str__(self):
        return self.request_number


# ---------------------------------------------------------------------------
# Expense Claim
# ---------------------------------------------------------------------------

class ExpenseClaim(models.Model):
    claim_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, related_name='expense_claims')
    travel_request = models.ForeignKey(
        TravelRequest, on_delete=models.SET_NULL, blank=True, null=True, related_name='expense_claims',
    )
    claim_date = models.DateField(blank=True, null=True)
    period_from = models.DateField(blank=True, null=True)
    period_to = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    advance_taken = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    balance_payable = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    receipts_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=ClaimStatus.choices, default=ClaimStatus.DRAFT)
    approver = models.CharField(max_length=150, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=60, blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Expense Claim'
        verbose_name_plural = 'Expense Claims'
        ordering = ['-created_at']

    def __str__(self):
        return self.claim_number


class ExpenseClaimItem(models.Model):
    claim = models.ForeignKey(ExpenseClaim, on_delete=models.CASCADE, related_name='items')
    expense_date = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=80, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    receipt = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Expense Claim Item'
        verbose_name_plural = 'Expense Claim Items'

    def __str__(self):
        return f"{self.claim.claim_number} - {self.category}"


# ---------------------------------------------------------------------------
# Employee Asset
# ---------------------------------------------------------------------------

class EmployeeAsset(models.Model):
    asset_code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=60, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=120, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    current_value = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_assets',
    )
    assigned_date = models.DateField(blank=True, null=True)
    expected_return = models.DateField(blank=True, null=True)
    condition = models.CharField(max_length=20, blank=True, null=True, help_text='excellent/good/fair/poor')
    status = models.CharField(max_length=20, choices=EmpAssetStatus.choices, default=EmpAssetStatus.AVAILABLE)
    warranty_expiry = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Employee Asset'
        verbose_name_plural = 'Employee Assets'
        ordering = ['asset_code']

    def __str__(self):
        return f"{self.asset_code} - {self.name}"
