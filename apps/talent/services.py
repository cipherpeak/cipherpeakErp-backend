from typing import Dict, Any, List
from .models import (
    JobOpening, Applicant, Interview, OnboardingRecord, OnboardingTask,
    ExitRecord, ExitClearanceItem, TrainingProgram, TrainingEnrollment,
    PerformanceReview, ReviewKPI, ReviewGoal, ReviewCompetency,
    TravelRequest, ExpenseClaim, ExpenseClaimItem, EmployeeAsset,
)


# ===========================================================================
# JOB OPENING SERVICES
# ===========================================================================

def get_all_job_openings() -> List[JobOpening]:
    return JobOpening.objects.filter(is_deleted=False)

def create_job_opening(data: Dict[str, Any]) -> JobOpening:
    job_code = data.get('job_code')
    if JobOpening.objects.filter(job_code__iexact=job_code).exists():
        raise ValueError(f"Job code '{job_code}' already exists.")
    return JobOpening.objects.create(**data)

def update_job_opening(job: JobOpening, data: Dict[str, Any]) -> JobOpening:
    job_code = data.get('job_code')
    if job_code and JobOpening.objects.filter(job_code__iexact=job_code).exclude(id=job.id).exists():
        raise ValueError(f"Job code '{job_code}' already exists.")
    for field, value in data.items():
        setattr(job, field, value)
    job.save()
    return job

def delete_job_opening(job: JobOpening) -> None:
    job.is_deleted = True
    job.save()


# ===========================================================================
# APPLICANT SERVICES
# ===========================================================================

def get_all_applicants() -> List[Applicant]:
    return Applicant.objects.filter(is_deleted=False)

def create_applicant(data: Dict[str, Any]) -> Applicant:
    applicant_number = data.get('applicant_number')
    if Applicant.objects.filter(applicant_number__iexact=applicant_number).exists():
        raise ValueError(f"Applicant number '{applicant_number}' already exists.")
    return Applicant.objects.create(**data)

def update_applicant(applicant: Applicant, data: Dict[str, Any]) -> Applicant:
    applicant_number = data.get('applicant_number')
    if applicant_number and Applicant.objects.filter(
        applicant_number__iexact=applicant_number,
    ).exclude(id=applicant.id).exists():
        raise ValueError(f"Applicant number '{applicant_number}' already exists.")
    for field, value in data.items():
        setattr(applicant, field, value)
    applicant.save()
    return applicant

def delete_applicant(applicant: Applicant) -> None:
    applicant.is_deleted = True
    applicant.save()


# ===========================================================================
# INTERVIEW SERVICES
# ===========================================================================

def get_all_interviews() -> List[Interview]:
    return Interview.objects.filter(is_deleted=False)

def create_interview(data: Dict[str, Any]) -> Interview:
    interview_number = data.get('interview_number')
    if Interview.objects.filter(interview_number__iexact=interview_number).exists():
        raise ValueError(f"Interview number '{interview_number}' already exists.")
    return Interview.objects.create(**data)

def update_interview(interview: Interview, data: Dict[str, Any]) -> Interview:
    interview_number = data.get('interview_number')
    if interview_number and Interview.objects.filter(
        interview_number__iexact=interview_number,
    ).exclude(id=interview.id).exists():
        raise ValueError(f"Interview number '{interview_number}' already exists.")
    for field, value in data.items():
        setattr(interview, field, value)
    interview.save()
    return interview

def delete_interview(interview: Interview) -> None:
    interview.is_deleted = True
    interview.save()


# ===========================================================================
# ONBOARDING SERVICES
# ===========================================================================

def get_all_onboarding_records() -> List[OnboardingRecord]:
    return OnboardingRecord.objects.filter(is_deleted=False)

def get_onboarding_with_tasks(onboarding_id: int) -> OnboardingRecord:
    return OnboardingRecord.objects.prefetch_related('tasks').get(pk=onboarding_id)

def create_onboarding_record(data: Dict[str, Any]) -> OnboardingRecord:
    onboarding_number = data.get('onboarding_number')
    if OnboardingRecord.objects.filter(onboarding_number__iexact=onboarding_number).exists():
        raise ValueError(f"Onboarding number '{onboarding_number}' already exists.")
    tasks_data = data.pop('tasks', [])
    record = OnboardingRecord.objects.create(**data)
    for task_data in tasks_data:
        OnboardingTask.objects.create(onboarding=record, **task_data)
    return record

def update_onboarding_record(record: OnboardingRecord, data: Dict[str, Any]) -> OnboardingRecord:
    onboarding_number = data.get('onboarding_number')
    if onboarding_number and OnboardingRecord.objects.filter(
        onboarding_number__iexact=onboarding_number,
    ).exclude(id=record.id).exists():
        raise ValueError(f"Onboarding number '{onboarding_number}' already exists.")
    data.pop('tasks', None)
    for field, value in data.items():
        setattr(record, field, value)
    record.save()
    return record

def delete_onboarding_record(record: OnboardingRecord) -> None:
    record.is_deleted = True
    record.save()


# ===========================================================================
# EXIT SERVICES
# ===========================================================================

def get_all_exit_records() -> List[ExitRecord]:
    return ExitRecord.objects.filter(is_deleted=False)

def get_exit_with_clearance(exit_id: int) -> ExitRecord:
    return ExitRecord.objects.prefetch_related('clearance_items').get(pk=exit_id)

def create_exit_record(data: Dict[str, Any]) -> ExitRecord:
    exit_number = data.get('exit_number')
    if ExitRecord.objects.filter(exit_number__iexact=exit_number).exists():
        raise ValueError(f"Exit number '{exit_number}' already exists.")
    items_data = data.pop('clearance_items', [])
    record = ExitRecord.objects.create(**data)
    for item_data in items_data:
        ExitClearanceItem.objects.create(exit_record=record, **item_data)
    return record

def update_exit_record(record: ExitRecord, data: Dict[str, Any]) -> ExitRecord:
    exit_number = data.get('exit_number')
    if exit_number and ExitRecord.objects.filter(
        exit_number__iexact=exit_number,
    ).exclude(id=record.id).exists():
        raise ValueError(f"Exit number '{exit_number}' already exists.")
    data.pop('clearance_items', None)
    for field, value in data.items():
        setattr(record, field, value)
    record.save()
    return record

def delete_exit_record(record: ExitRecord) -> None:
    record.is_deleted = True
    record.save()


# ===========================================================================
# TRAINING SERVICES
# ===========================================================================

def get_all_training_programs() -> List[TrainingProgram]:
    return TrainingProgram.objects.filter(is_deleted=False)

def get_training_with_enrollments(program_id: int) -> TrainingProgram:
    return TrainingProgram.objects.prefetch_related('enrollments').get(pk=program_id)

def create_training_program(data: Dict[str, Any]) -> TrainingProgram:
    program_code = data.get('program_code')
    if TrainingProgram.objects.filter(program_code__iexact=program_code).exists():
        raise ValueError(f"Program code '{program_code}' already exists.")
    enrollments_data = data.pop('enrollments', [])
    program = TrainingProgram.objects.create(**data)
    for enr_data in enrollments_data:
        TrainingEnrollment.objects.create(program=program, **enr_data)
    return program

def update_training_program(program: TrainingProgram, data: Dict[str, Any]) -> TrainingProgram:
    program_code = data.get('program_code')
    if program_code and TrainingProgram.objects.filter(
        program_code__iexact=program_code,
    ).exclude(id=program.id).exists():
        raise ValueError(f"Program code '{program_code}' already exists.")
    data.pop('enrollments', None)
    for field, value in data.items():
        setattr(program, field, value)
    program.save()
    return program

def delete_training_program(program: TrainingProgram) -> None:
    program.is_deleted = True
    program.save()


# ===========================================================================
# PERFORMANCE REVIEW SERVICES
# ===========================================================================

def get_all_performance_reviews() -> List[PerformanceReview]:
    return PerformanceReview.objects.filter(is_deleted=False)

def get_review_with_details(review_id: int) -> PerformanceReview:
    return PerformanceReview.objects.prefetch_related('kpis', 'goals', 'competencies').get(pk=review_id)

def create_performance_review(data: Dict[str, Any]) -> PerformanceReview:
    review_number = data.get('review_number')
    if PerformanceReview.objects.filter(review_number__iexact=review_number).exists():
        raise ValueError(f"Review number '{review_number}' already exists.")
    kpis_data = data.pop('kpis', [])
    goals_data = data.pop('goals', [])
    competencies_data = data.pop('competencies', [])
    review = PerformanceReview.objects.create(**data)
    for kpi_data in kpis_data:
        ReviewKPI.objects.create(review=review, **kpi_data)
    for goal_data in goals_data:
        ReviewGoal.objects.create(review=review, **goal_data)
    for comp_data in competencies_data:
        ReviewCompetency.objects.create(review=review, **comp_data)
    return review

def update_performance_review(review: PerformanceReview, data: Dict[str, Any]) -> PerformanceReview:
    review_number = data.get('review_number')
    if review_number and PerformanceReview.objects.filter(
        review_number__iexact=review_number,
    ).exclude(id=review.id).exists():
        raise ValueError(f"Review number '{review_number}' already exists.")
    data.pop('kpis', None)
    data.pop('goals', None)
    data.pop('competencies', None)
    for field, value in data.items():
        setattr(review, field, value)
    review.save()
    return review

def delete_performance_review(review: PerformanceReview) -> None:
    review.is_deleted = True
    review.save()


# ===========================================================================
# TRAVEL REQUEST SERVICES
# ===========================================================================

def get_all_travel_requests() -> List[TravelRequest]:
    return TravelRequest.objects.filter(is_deleted=False)

def create_travel_request(data: Dict[str, Any]) -> TravelRequest:
    request_number = data.get('request_number')
    if TravelRequest.objects.filter(request_number__iexact=request_number).exists():
        raise ValueError(f"Request number '{request_number}' already exists.")
    return TravelRequest.objects.create(**data)

def update_travel_request(travel: TravelRequest, data: Dict[str, Any]) -> TravelRequest:
    request_number = data.get('request_number')
    if request_number and TravelRequest.objects.filter(
        request_number__iexact=request_number,
    ).exclude(id=travel.id).exists():
        raise ValueError(f"Request number '{request_number}' already exists.")
    for field, value in data.items():
        setattr(travel, field, value)
    travel.save()
    return travel

def delete_travel_request(travel: TravelRequest) -> None:
    travel.is_deleted = True
    travel.save()


# ===========================================================================
# EXPENSE CLAIM SERVICES
# ===========================================================================

def get_all_expense_claims() -> List[ExpenseClaim]:
    return ExpenseClaim.objects.filter(is_deleted=False)

def get_claim_with_items(claim_id: int) -> ExpenseClaim:
    return ExpenseClaim.objects.prefetch_related('items').get(pk=claim_id)

def create_expense_claim(data: Dict[str, Any]) -> ExpenseClaim:
    claim_number = data.get('claim_number')
    if ExpenseClaim.objects.filter(claim_number__iexact=claim_number).exists():
        raise ValueError(f"Claim number '{claim_number}' already exists.")
    items_data = data.pop('items', [])
    claim = ExpenseClaim.objects.create(**data)
    for item_data in items_data:
        ExpenseClaimItem.objects.create(claim=claim, **item_data)
    return claim

def update_expense_claim(claim: ExpenseClaim, data: Dict[str, Any]) -> ExpenseClaim:
    claim_number = data.get('claim_number')
    if claim_number and ExpenseClaim.objects.filter(
        claim_number__iexact=claim_number,
    ).exclude(id=claim.id).exists():
        raise ValueError(f"Claim number '{claim_number}' already exists.")
    data.pop('items', None)
    for field, value in data.items():
        setattr(claim, field, value)
    claim.save()
    return claim

def delete_expense_claim(claim: ExpenseClaim) -> None:
    claim.is_deleted = True
    claim.save()


# ===========================================================================
# EMPLOYEE ASSET SERVICES
# ===========================================================================

def get_all_employee_assets() -> List[EmployeeAsset]:
    return EmployeeAsset.objects.filter(is_deleted=False)

def create_employee_asset(data: Dict[str, Any]) -> EmployeeAsset:
    asset_code = data.get('asset_code')
    if EmployeeAsset.objects.filter(asset_code__iexact=asset_code).exists():
        raise ValueError(f"Asset code '{asset_code}' already exists.")
    return EmployeeAsset.objects.create(**data)

def update_employee_asset(asset: EmployeeAsset, data: Dict[str, Any]) -> EmployeeAsset:
    asset_code = data.get('asset_code')
    if asset_code and EmployeeAsset.objects.filter(asset_code__iexact=asset_code).exclude(id=asset.id).exists():
        raise ValueError(f"Asset code '{asset_code}' already exists.")
    for field, value in data.items():
        setattr(asset, field, value)
    asset.save()
    return asset

def delete_employee_asset(asset: EmployeeAsset) -> None:
    asset.is_deleted = True
    asset.save()
