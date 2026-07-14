from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    JobOpening, Applicant, Interview, OnboardingRecord, ExitRecord,
    TrainingProgram, PerformanceReview, TravelRequest, ExpenseClaim, EmployeeAsset,
)
from .serializers import (
    JobOpeningSerializer, ApplicantSerializer, InterviewSerializer,
    OnboardingRecordSerializer, ExitRecordSerializer, TrainingProgramSerializer,
    PerformanceReviewSerializer, TravelRequestSerializer, ExpenseClaimSerializer,
    EmployeeAssetSerializer,
)
from . import services


# ===========================================================================
# JOB OPENING VIEWSET
# ===========================================================================

class JobOpeningViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        jobs = services.get_all_job_openings()
        return Response(JobOpeningSerializer(jobs, many=True).data)

    def retrieve(self, request, pk=None):
        job = get_object_or_404(JobOpening, pk=pk)
        return Response(JobOpeningSerializer(job).data)

    def create(self, request):
        serializer = JobOpeningSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_job_opening(serializer.validated_data)
            return Response({"message": "Job opening created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        job = get_object_or_404(JobOpening, pk=pk)
        serializer = JobOpeningSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_job_opening(job, serializer.validated_data)
            return Response({"message": "Job opening updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        job = get_object_or_404(JobOpening, pk=pk)
        serializer = JobOpeningSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_job_opening(job, serializer.validated_data)
            return Response({"message": "Job opening updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        job = get_object_or_404(JobOpening, pk=pk)
        services.delete_job_opening(job)
        return Response({"message": "Job opening deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# APPLICANT VIEWSET
# ===========================================================================

class ApplicantViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        applicants = services.get_all_applicants()
        return Response(ApplicantSerializer(applicants, many=True).data)

    def retrieve(self, request, pk=None):
        applicant = get_object_or_404(Applicant, pk=pk)
        return Response(ApplicantSerializer(applicant).data)

    def create(self, request):
        serializer = ApplicantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_applicant(serializer.validated_data)
            return Response({"message": "Applicant created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        applicant = get_object_or_404(Applicant, pk=pk)
        serializer = ApplicantSerializer(applicant, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_applicant(applicant, serializer.validated_data)
            return Response({"message": "Applicant updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        applicant = get_object_or_404(Applicant, pk=pk)
        serializer = ApplicantSerializer(applicant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_applicant(applicant, serializer.validated_data)
            return Response({"message": "Applicant updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        applicant = get_object_or_404(Applicant, pk=pk)
        services.delete_applicant(applicant)
        return Response({"message": "Applicant deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# INTERVIEW VIEWSET
# ===========================================================================

class InterviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        interviews = services.get_all_interviews()
        return Response(InterviewSerializer(interviews, many=True).data)

    def retrieve(self, request, pk=None):
        interview = get_object_or_404(Interview, pk=pk)
        return Response(InterviewSerializer(interview).data)

    def create(self, request):
        serializer = InterviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_interview(serializer.validated_data)
            return Response({"message": "Interview created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        interview = get_object_or_404(Interview, pk=pk)
        serializer = InterviewSerializer(interview, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_interview(interview, serializer.validated_data)
            return Response({"message": "Interview updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        interview = get_object_or_404(Interview, pk=pk)
        serializer = InterviewSerializer(interview, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_interview(interview, serializer.validated_data)
            return Response({"message": "Interview updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        interview = get_object_or_404(Interview, pk=pk)
        services.delete_interview(interview)
        return Response({"message": "Interview deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# ONBOARDING VIEWSET
# ===========================================================================

class OnboardingRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        records = services.get_all_onboarding_records()
        return Response(OnboardingRecordSerializer(records, many=True).data)

    def retrieve(self, request, pk=None):
        record = services.get_onboarding_with_tasks(pk)
        return Response(OnboardingRecordSerializer(record).data)

    def create(self, request):
        serializer = OnboardingRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_onboarding_record(serializer.validated_data)
            return Response({"message": "Onboarding record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        record = get_object_or_404(OnboardingRecord, pk=pk)
        serializer = OnboardingRecordSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_onboarding_record(record, serializer.validated_data)
            return Response({"message": "Onboarding record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        record = get_object_or_404(OnboardingRecord, pk=pk)
        serializer = OnboardingRecordSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_onboarding_record(record, serializer.validated_data)
            return Response({"message": "Onboarding record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        record = get_object_or_404(OnboardingRecord, pk=pk)
        services.delete_onboarding_record(record)
        return Response({"message": "Onboarding record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# EXIT RECORD VIEWSET
# ===========================================================================

class ExitRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        records = services.get_all_exit_records()
        return Response(ExitRecordSerializer(records, many=True).data)

    def retrieve(self, request, pk=None):
        record = services.get_exit_with_clearance(pk)
        return Response(ExitRecordSerializer(record).data)

    def create(self, request):
        serializer = ExitRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_exit_record(serializer.validated_data)
            return Response({"message": "Exit record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        record = get_object_or_404(ExitRecord, pk=pk)
        serializer = ExitRecordSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_exit_record(record, serializer.validated_data)
            return Response({"message": "Exit record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        record = get_object_or_404(ExitRecord, pk=pk)
        serializer = ExitRecordSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_exit_record(record, serializer.validated_data)
            return Response({"message": "Exit record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        record = get_object_or_404(ExitRecord, pk=pk)
        services.delete_exit_record(record)
        return Response({"message": "Exit record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TRAINING PROGRAM VIEWSET
# ===========================================================================

class TrainingProgramViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        programs = services.get_all_training_programs()
        return Response(TrainingProgramSerializer(programs, many=True).data)

    def retrieve(self, request, pk=None):
        program = services.get_training_with_enrollments(pk)
        return Response(TrainingProgramSerializer(program).data)

    def create(self, request):
        serializer = TrainingProgramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_training_program(serializer.validated_data)
            return Response({"message": "Training program created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        program = get_object_or_404(TrainingProgram, pk=pk)
        serializer = TrainingProgramSerializer(program, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_training_program(program, serializer.validated_data)
            return Response({"message": "Training program updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        program = get_object_or_404(TrainingProgram, pk=pk)
        serializer = TrainingProgramSerializer(program, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_training_program(program, serializer.validated_data)
            return Response({"message": "Training program updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        program = get_object_or_404(TrainingProgram, pk=pk)
        services.delete_training_program(program)
        return Response({"message": "Training program deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PERFORMANCE REVIEW VIEWSET
# ===========================================================================

class PerformanceReviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        reviews = services.get_all_performance_reviews()
        return Response(PerformanceReviewSerializer(reviews, many=True).data)

    def retrieve(self, request, pk=None):
        review = services.get_review_with_details(pk)
        return Response(PerformanceReviewSerializer(review).data)

    def create(self, request):
        serializer = PerformanceReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_performance_review(serializer.validated_data)
            return Response({"message": "Performance review created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        review = get_object_or_404(PerformanceReview, pk=pk)
        serializer = PerformanceReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_performance_review(review, serializer.validated_data)
            return Response({"message": "Performance review updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        review = get_object_or_404(PerformanceReview, pk=pk)
        serializer = PerformanceReviewSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_performance_review(review, serializer.validated_data)
            return Response({"message": "Performance review updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        review = get_object_or_404(PerformanceReview, pk=pk)
        services.delete_performance_review(review)
        return Response({"message": "Performance review deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TRAVEL REQUEST VIEWSET
# ===========================================================================

class TravelRequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        travels = services.get_all_travel_requests()
        return Response(TravelRequestSerializer(travels, many=True).data)

    def retrieve(self, request, pk=None):
        travel = get_object_or_404(TravelRequest, pk=pk)
        return Response(TravelRequestSerializer(travel).data)

    def create(self, request):
        serializer = TravelRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_travel_request(serializer.validated_data)
            return Response({"message": "Travel request created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        travel = get_object_or_404(TravelRequest, pk=pk)
        serializer = TravelRequestSerializer(travel, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_travel_request(travel, serializer.validated_data)
            return Response({"message": "Travel request updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        travel = get_object_or_404(TravelRequest, pk=pk)
        serializer = TravelRequestSerializer(travel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_travel_request(travel, serializer.validated_data)
            return Response({"message": "Travel request updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        travel = get_object_or_404(TravelRequest, pk=pk)
        services.delete_travel_request(travel)
        return Response({"message": "Travel request deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# EXPENSE CLAIM VIEWSET
# ===========================================================================

class ExpenseClaimViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        claims = services.get_all_expense_claims()
        return Response(ExpenseClaimSerializer(claims, many=True).data)

    def retrieve(self, request, pk=None):
        claim = services.get_claim_with_items(pk)
        return Response(ExpenseClaimSerializer(claim).data)

    def create(self, request):
        serializer = ExpenseClaimSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_expense_claim(serializer.validated_data)
            return Response({"message": "Expense claim created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        claim = get_object_or_404(ExpenseClaim, pk=pk)
        serializer = ExpenseClaimSerializer(claim, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_expense_claim(claim, serializer.validated_data)
            return Response({"message": "Expense claim updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        claim = get_object_or_404(ExpenseClaim, pk=pk)
        serializer = ExpenseClaimSerializer(claim, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_expense_claim(claim, serializer.validated_data)
            return Response({"message": "Expense claim updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        claim = get_object_or_404(ExpenseClaim, pk=pk)
        services.delete_expense_claim(claim)
        return Response({"message": "Expense claim deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# EMPLOYEE ASSET VIEWSET
# ===========================================================================

class EmployeeAssetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        assets = services.get_all_employee_assets()
        return Response(EmployeeAssetSerializer(assets, many=True).data)

    def retrieve(self, request, pk=None):
        asset = get_object_or_404(EmployeeAsset, pk=pk)
        return Response(EmployeeAssetSerializer(asset).data)

    def create(self, request):
        serializer = EmployeeAssetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_employee_asset(serializer.validated_data)
            return Response({"message": "Employee asset created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        asset = get_object_or_404(EmployeeAsset, pk=pk)
        serializer = EmployeeAssetSerializer(asset, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_employee_asset(asset, serializer.validated_data)
            return Response({"message": "Employee asset updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        asset = get_object_or_404(EmployeeAsset, pk=pk)
        serializer = EmployeeAssetSerializer(asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_employee_asset(asset, serializer.validated_data)
            return Response({"message": "Employee asset updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        asset = get_object_or_404(EmployeeAsset, pk=pk)
        services.delete_employee_asset(asset)
        return Response({"message": "Employee asset deleted successfully."}, status=status.HTTP_200_OK)
