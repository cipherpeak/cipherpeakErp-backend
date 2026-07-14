from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'jurisdictions', views.TaxJurisdictionViewSet, basename='tax-jurisdiction')
router.register(r'tax-types', views.TaxTypeViewSet, basename='tax-type')
router.register(r'hsn-codes', views.HSNCodeViewSet, basename='hsn-code')
router.register(r'tax-rates', views.TaxRateViewSet, basename='tax-rate')
router.register(r'tax-categories', views.TaxCategoryViewSet, basename='tax-category')
router.register(r'tax-groups', views.TaxGroupViewSet, basename='tax-group')
router.register(r'tax-rules', views.TaxRuleViewSet, basename='tax-rule')
router.register(r'exemptions', views.TaxExemptionViewSet, basename='tax-exemption')
router.register(r'reverse-charges', views.ReverseChargeRecordViewSet, basename='reverse-charge')
router.register(r'tax-returns', views.TaxReturnViewSet, basename='tax-return')
router.register(r'mapping-rules', views.TaxMappingRuleViewSet, basename='tax-mapping-rule')

urlpatterns = [
    path('', include(router.urls)),
]
