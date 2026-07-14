from rest_framework import serializers
from .models import (
    JobOpening, Applicant, Interview, OnboardingRecord, OnboardingTask,
    ExitRecord, ExitClearanceItem, TrainingProgram, TrainingEnrollment,
    PerformanceReview, ReviewKPI, ReviewGoal, ReviewCompetency,
    TravelRequest, ExpenseClaim, ExpenseClaimItem, EmployeeAsset,
)


# ===========================================================================
# JOB OPENING SERIALIZER
# ===========================================================================

class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = '__all__'


# ===========================================================================
# APPLICANT SERIALIZER
# ===========================================================================

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


# ===========================================================================
# INTERVIEW SERIALIZER
# ===========================================================================

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'


# ===========================================================================
# ONBOARDING SERIALIZERS
# ===========================================================================

class OnboardingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTask
        fields = '__all__'
        extra_kwargs = {'onboarding': {'required': False}}


class OnboardingRecordSerializer(serializers.ModelSerializer):
    tasks = OnboardingTaskSerializer(many=True, required=False)

    class Meta:
        model = OnboardingRecord
        fields = '__all__'


# ===========================================================================
# EXIT SERIALIZERS
# ===========================================================================

class ExitClearanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExitClearanceItem
        fields = '__all__'
        extra_kwargs = {'exit_record': {'required': False}}


class ExitRecordSerializer(serializers.ModelSerializer):
    clearance_items = ExitClearanceItemSerializer(many=True, required=False)

    class Meta:
        model = ExitRecord
        fields = '__all__'


# ===========================================================================
# TRAINING SERIALIZERS
# ===========================================================================

class TrainingEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingEnrollment
        fields = '__all__'
        extra_kwargs = {'program': {'required': False}}


class TrainingProgramSerializer(serializers.ModelSerializer):
    enrollments = TrainingEnrollmentSerializer(many=True, required=False)

    class Meta:
        model = TrainingProgram
        fields = '__all__'


# ===========================================================================
# PERFORMANCE REVIEW SERIALIZERS
# ===========================================================================

class ReviewKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewKPI
        fields = '__all__'
        extra_kwargs = {'review': {'required': False}}


class ReviewGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewGoal
        fields = '__all__'
        extra_kwargs = {'review': {'required': False}}


class ReviewCompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCompetency
        fields = '__all__'
        extra_kwargs = {'review': {'required': False}}


class PerformanceReviewSerializer(serializers.ModelSerializer):
    kpis = ReviewKPISerializer(many=True, required=False)
    goals = ReviewGoalSerializer(many=True, required=False)
    competencies = ReviewCompetencySerializer(many=True, required=False)

    class Meta:
        model = PerformanceReview
        fields = '__all__'


# ===========================================================================
# TRAVEL REQUEST SERIALIZER
# ===========================================================================

class TravelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelRequest
        fields = '__all__'


# ===========================================================================
# EXPENSE CLAIM SERIALIZERS
# ===========================================================================

class ExpenseClaimItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseClaimItem
        fields = '__all__'
        extra_kwargs = {'claim': {'required': False}}


class ExpenseClaimSerializer(serializers.ModelSerializer):
    items = ExpenseClaimItemSerializer(many=True, required=False)

    class Meta:
        model = ExpenseClaim
        fields = '__all__'


# ===========================================================================
# EMPLOYEE ASSET SERIALIZER
# ===========================================================================

class EmployeeAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAsset
        fields = '__all__'
