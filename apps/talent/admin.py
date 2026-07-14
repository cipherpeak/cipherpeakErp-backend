from django.contrib import admin
from .models import (
    JobOpening, Applicant, Interview, OnboardingRecord, OnboardingTask,
    ExitRecord, ExitClearanceItem, TrainingProgram, TrainingEnrollment,
    PerformanceReview, ReviewKPI, ReviewGoal, ReviewCompetency,
    TravelRequest, ExpenseClaim, ExpenseClaimItem, EmployeeAsset,
)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('job_code', 'title', 'department_name', 'location', 'employment_type', 'posted_date', 'closing_date', 'status', 'created_at')
    search_fields = ('job_code', 'title', 'location')
    list_filter = ('status', 'employment_type')


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('applicant_number', 'name', 'job_opening', 'email', 'phone', 'source', 'status', 'rating', 'applied_date', 'created_at')
    search_fields = ('applicant_number', 'name', 'email')
    list_filter = ('status', 'source', 'gender')


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('interview_number', 'applicant', 'round', 'scheduled_date', 'scheduled_time', 'mode', 'status', 'overall_rating', 'recommendation', 'created_at')
    search_fields = ('interview_number', 'round')
    list_filter = ('status', 'mode')


class OnboardingTaskInline(admin.TabularInline):
    model = OnboardingTask
    extra = 0


@admin.register(OnboardingRecord)
class OnboardingRecordAdmin(admin.ModelAdmin):
    list_display = ('onboarding_number', 'employee', 'join_date', 'status', 'buddy', 'manager', 'completion_percentage', 'created_at')
    search_fields = ('onboarding_number', 'buddy', 'manager')
    list_filter = ('status',)
    inlines = [OnboardingTaskInline]


class ExitClearanceItemInline(admin.TabularInline):
    model = ExitClearanceItem
    extra = 0


@admin.register(ExitRecord)
class ExitRecordAdmin(admin.ModelAdmin):
    list_display = ('exit_number', 'employee', 'exit_type', 'status', 'last_working_day', 'total_payable', 'created_at')
    search_fields = ('exit_number',)
    list_filter = ('exit_type', 'status')
    inlines = [ExitClearanceItemInline]


class TrainingEnrollmentInline(admin.TabularInline):
    model = TrainingEnrollment
    extra = 0


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('program_code', 'title', 'category', 'trainer', 'mode', 'start_date', 'end_date', 'capacity', 'enrolled', 'status', 'created_at')
    search_fields = ('program_code', 'title', 'trainer')
    list_filter = ('status', 'mode', 'certification')
    inlines = [TrainingEnrollmentInline]


class ReviewKPIInline(admin.TabularInline):
    model = ReviewKPI
    extra = 0


class ReviewGoalInline(admin.TabularInline):
    model = ReviewGoal
    extra = 0


class ReviewCompetencyInline(admin.TabularInline):
    model = ReviewCompetency
    extra = 0


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('review_number', 'employee', 'manager', 'review_period', 'review_type', 'status', 'overall_rating', 'created_at')
    search_fields = ('review_number', 'manager', 'review_period')
    list_filter = ('review_type', 'status')
    inlines = [ReviewKPIInline, ReviewGoalInline, ReviewCompetencyInline]


@admin.register(TravelRequest)
class TravelRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'employee', 'destination_city', 'destination_country', 'travel_date', 'return_date', 'estimated_total', 'status', 'created_at')
    search_fields = ('request_number', 'destination_city', 'destination_country')
    list_filter = ('status',)


class ExpenseClaimItemInline(admin.TabularInline):
    model = ExpenseClaimItem
    extra = 0


@admin.register(ExpenseClaim)
class ExpenseClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_number', 'employee', 'claim_date', 'total_amount', 'advance_taken', 'balance_payable', 'status', 'created_at')
    search_fields = ('claim_number',)
    list_filter = ('status',)
    inlines = [ExpenseClaimItemInline]


@admin.register(EmployeeAsset)
class EmployeeAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_code', 'name', 'category', 'brand', 'model', 'serial_number', 'assigned_to', 'assigned_date', 'condition', 'status', 'created_at')
    search_fields = ('asset_code', 'name', 'serial_number')
    list_filter = ('status', 'category', 'condition')
