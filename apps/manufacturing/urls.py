from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'machine-categories', views.MachineCategoryViewSet, basename='machine-category')
router.register(r'machines', views.MachineViewSet, basename='machine')
router.register(r'production-lines', views.ProductionLineViewSet, basename='production-line')
router.register(r'work-centers', views.WorkCenterViewSet, basename='work-center')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'bom-categories', views.BOMCategoryViewSet, basename='bom-category')
router.register(r'boms', views.BillOfMaterialViewSet, basename='bom')
router.register(r'bom-versions', views.BOMVersionViewSet, basename='bom-version')
router.register(r'bom-substitutions', views.BOMSubstitutionViewSet, basename='bom-substitution')
router.register(r'production-plans', views.ProductionPlanViewSet, basename='production-plan')
router.register(r'work-orders', views.WorkOrderViewSet, basename='work-order')
router.register(r'job-cards', views.JobCardViewSet, basename='job-card')
router.register(r'production-tracking', views.ProductionTrackingViewSet, basename='production-tracking')

urlpatterns = [
    path('', include(router.urls)),
]
