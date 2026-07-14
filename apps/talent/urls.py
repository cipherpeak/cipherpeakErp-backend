from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'job-openings', views.JobOpeningViewSet, basename='job-opening')
router.register(r'applicants', views.ApplicantViewSet, basename='applicant')
router.register(r'interviews', views.InterviewViewSet, basename='interview')
router.register(r'onboarding', views.OnboardingRecordViewSet, basename='onboarding')
router.register(r'exits', views.ExitRecordViewSet, basename='exit')
router.register(r'training-programs', views.TrainingProgramViewSet, basename='training-program')
router.register(r'performance-reviews', views.PerformanceReviewViewSet, basename='performance-review')
router.register(r'travel-requests', views.TravelRequestViewSet, basename='travel-request')
router.register(r'expense-claims', views.ExpenseClaimViewSet, basename='expense-claim')
router.register(r'employee-assets', views.EmployeeAssetViewSet, basename='employee-asset')

urlpatterns = [
    path('', include(router.urls)),
]
