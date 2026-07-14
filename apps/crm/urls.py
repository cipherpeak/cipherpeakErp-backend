from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='crm-account')
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'leads', views.LeadViewSet, basename='lead')
router.register(r'opportunities', views.OpportunityViewSet, basename='opportunity')
router.register(r'activities', views.CRMActivityViewSet, basename='crm-activity')
router.register(r'quotations', views.CRMQuotationViewSet, basename='crm-quotation')

urlpatterns = [
    path('', include(router.urls)),
]
