from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    MachineCategory, Machine, ProductionLine, WorkCenter, Product,
    BOMCategory, BillOfMaterial, BOMMaterial, BOMOperation, BOMVersion, BOMSubstitution,
    ProductionPlan, ProductionPlanMaterial, WorkOrder, WorkOrderMaterial,
    WorkOrderOperation, WorkOrderQualityCheck, JobCard, ProductionTracking,
)
from .serializers import (
    MachineCategorySerializer, MachineSerializer, ProductionLineSerializer,
    WorkCenterSerializer, ProductSerializer, BOMCategorySerializer,
    BillOfMaterialSerializer, BOMMaterialSerializer, BOMOperationSerializer,
    BOMVersionSerializer, BOMSubstitutionSerializer,
    ProductionPlanSerializer, ProductionPlanMaterialSerializer,
    WorkOrderSerializer, WorkOrderMaterialSerializer,
    WorkOrderOperationSerializer, WorkOrderQualityCheckSerializer,
    JobCardSerializer, ProductionTrackingSerializer,
)
from . import services


# ===========================================================================
# MACHINE CATEGORY VIEWSET
# ===========================================================================

class MachineCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories = services.get_all_machine_categories()
        serializer = MachineCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(MachineCategory, pk=pk)
        serializer = MachineCategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = MachineCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_machine_category(serializer.validated_data)
            return Response({"message": "Machine category created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = get_object_or_404(MachineCategory, pk=pk)
        serializer = MachineCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_machine_category(category, serializer.validated_data)
            return Response({"message": "Machine category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = get_object_or_404(MachineCategory, pk=pk)
        serializer = MachineCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_machine_category(category, serializer.validated_data)
            return Response({"message": "Machine category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = get_object_or_404(MachineCategory, pk=pk)
        services.delete_machine_category(category)
        return Response({"message": "Machine category deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# MACHINE VIEWSET
# ===========================================================================

class MachineViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        machines = services.get_all_machines()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        machine = get_object_or_404(Machine, pk=pk)
        serializer = MachineSerializer(machine)
        return Response(serializer.data)

    def create(self, request):
        serializer = MachineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_machine(serializer.validated_data)
            return Response({"message": "Machine created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        machine = get_object_or_404(Machine, pk=pk)
        serializer = MachineSerializer(machine, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_machine(machine, serializer.validated_data)
            return Response({"message": "Machine updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        machine = get_object_or_404(Machine, pk=pk)
        serializer = MachineSerializer(machine, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_machine(machine, serializer.validated_data)
            return Response({"message": "Machine updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        machine = get_object_or_404(Machine, pk=pk)
        services.delete_machine(machine)
        return Response({"message": "Machine deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PRODUCTION LINE VIEWSET
# ===========================================================================

class ProductionLineViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        lines = services.get_all_production_lines()
        serializer = ProductionLineSerializer(lines, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        line = get_object_or_404(ProductionLine, pk=pk)
        serializer = ProductionLineSerializer(line)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductionLineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_production_line(serializer.validated_data)
            return Response({"message": "Production line created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        line = get_object_or_404(ProductionLine, pk=pk)
        serializer = ProductionLineSerializer(line, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_production_line(line, serializer.validated_data)
            return Response({"message": "Production line updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        line = get_object_or_404(ProductionLine, pk=pk)
        serializer = ProductionLineSerializer(line, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_production_line(line, serializer.validated_data)
            return Response({"message": "Production line updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        line = get_object_or_404(ProductionLine, pk=pk)
        services.delete_production_line(line)
        return Response({"message": "Production line deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# WORK CENTER VIEWSET
# ===========================================================================

class WorkCenterViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        centers = services.get_all_work_centers()
        serializer = WorkCenterSerializer(centers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        center = get_object_or_404(WorkCenter, pk=pk)
        serializer = WorkCenterSerializer(center)
        return Response(serializer.data)

    def create(self, request):
        serializer = WorkCenterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_work_center(serializer.validated_data)
            return Response({"message": "Work center created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        center = get_object_or_404(WorkCenter, pk=pk)
        serializer = WorkCenterSerializer(center, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_work_center(center, serializer.validated_data)
            return Response({"message": "Work center updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        center = get_object_or_404(WorkCenter, pk=pk)
        serializer = WorkCenterSerializer(center, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_work_center(center, serializer.validated_data)
            return Response({"message": "Work center updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        center = get_object_or_404(WorkCenter, pk=pk)
        services.delete_work_center(center)
        return Response({"message": "Work center deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PRODUCT VIEWSET
# ===========================================================================

class ProductViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        products = services.get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_product(serializer.validated_data)
            return Response({"message": "Product created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_product(product, serializer.validated_data)
            return Response({"message": "Product updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_product(product, serializer.validated_data)
            return Response({"message": "Product updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        services.delete_product(product)
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BOM CATEGORY VIEWSET
# ===========================================================================

class BOMCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories = services.get_all_bom_categories()
        serializer = BOMCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(BOMCategory, pk=pk)
        serializer = BOMCategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = BOMCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bom_category(serializer.validated_data)
            return Response({"message": "BOM category created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = get_object_or_404(BOMCategory, pk=pk)
        serializer = BOMCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bom_category(category, serializer.validated_data)
            return Response({"message": "BOM category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = get_object_or_404(BOMCategory, pk=pk)
        serializer = BOMCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bom_category(category, serializer.validated_data)
            return Response({"message": "BOM category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = get_object_or_404(BOMCategory, pk=pk)
        services.delete_bom_category(category)
        return Response({"message": "BOM category deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BILL OF MATERIALS VIEWSET
# ===========================================================================

class BillOfMaterialViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        boms = services.get_all_boms()
        serializer = BillOfMaterialSerializer(boms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        bom = services.get_bom_with_details(pk)
        serializer = BillOfMaterialSerializer(bom)
        return Response(serializer.data)

    def create(self, request):
        serializer = BillOfMaterialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bom(serializer.validated_data)
            return Response({"message": "BOM created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        bom = get_object_or_404(BillOfMaterial, pk=pk)
        serializer = BillOfMaterialSerializer(bom, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bom(bom, serializer.validated_data)
            return Response({"message": "BOM updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        bom = get_object_or_404(BillOfMaterial, pk=pk)
        serializer = BillOfMaterialSerializer(bom, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bom(bom, serializer.validated_data)
            return Response({"message": "BOM updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        bom = get_object_or_404(BillOfMaterial, pk=pk)
        services.delete_bom(bom)
        return Response({"message": "BOM deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BOM VERSION VIEWSET
# ===========================================================================

class BOMVersionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        versions = services.get_all_bom_versions()
        serializer = BOMVersionSerializer(versions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BOMVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bom_version(serializer.validated_data)
            return Response({"message": "BOM version created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        version = get_object_or_404(BOMVersion, pk=pk)
        services.delete_bom_version(version)
        return Response({"message": "BOM version deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BOM SUBSTITUTION VIEWSET
# ===========================================================================

class BOMSubstitutionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        substitutions = services.get_all_bom_substitutions()
        serializer = BOMSubstitutionSerializer(substitutions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BOMSubstitutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_bom_substitution(serializer.validated_data)
            return Response({"message": "BOM substitution created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        sub = get_object_or_404(BOMSubstitution, pk=pk)
        serializer = BOMSubstitutionSerializer(sub, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_bom_substitution(sub, serializer.validated_data)
            return Response({"message": "BOM substitution updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sub = get_object_or_404(BOMSubstitution, pk=pk)
        services.delete_bom_substitution(sub)
        return Response({"message": "BOM substitution deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PRODUCTION PLAN VIEWSET
# ===========================================================================

class ProductionPlanViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        plans = services.get_all_production_plans()
        serializer = ProductionPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        plan = services.get_production_plan_with_materials(pk)
        serializer = ProductionPlanSerializer(plan)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductionPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_production_plan(serializer.validated_data)
            return Response({"message": "Production plan created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        plan = get_object_or_404(ProductionPlan, pk=pk)
        serializer = ProductionPlanSerializer(plan, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_production_plan(plan, serializer.validated_data)
            return Response({"message": "Production plan updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        plan = get_object_or_404(ProductionPlan, pk=pk)
        serializer = ProductionPlanSerializer(plan, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_production_plan(plan, serializer.validated_data)
            return Response({"message": "Production plan updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        plan = get_object_or_404(ProductionPlan, pk=pk)
        services.delete_production_plan(plan)
        return Response({"message": "Production plan deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# WORK ORDER VIEWSET
# ===========================================================================

class WorkOrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        wos = services.get_all_work_orders()
        serializer = WorkOrderSerializer(wos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        wo = services.get_work_order_with_details(pk)
        serializer = WorkOrderSerializer(wo)
        return Response(serializer.data)

    def create(self, request):
        serializer = WorkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_work_order(serializer.validated_data)
            return Response({"message": "Work order created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        wo = get_object_or_404(WorkOrder, pk=pk)
        serializer = WorkOrderSerializer(wo, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_work_order(wo, serializer.validated_data)
            return Response({"message": "Work order updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        wo = get_object_or_404(WorkOrder, pk=pk)
        serializer = WorkOrderSerializer(wo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_work_order(wo, serializer.validated_data)
            return Response({"message": "Work order updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        wo = get_object_or_404(WorkOrder, pk=pk)
        services.delete_work_order(wo)
        return Response({"message": "Work order deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# JOB CARD VIEWSET
# ===========================================================================

class JobCardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cards = services.get_all_job_cards()
        serializer = JobCardSerializer(cards, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        card = get_object_or_404(JobCard, pk=pk)
        serializer = JobCardSerializer(card)
        return Response(serializer.data)

    def create(self, request):
        serializer = JobCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_job_card(serializer.validated_data)
            return Response({"message": "Job card created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        card = get_object_or_404(JobCard, pk=pk)
        serializer = JobCardSerializer(card, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_job_card(card, serializer.validated_data)
            return Response({"message": "Job card updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        card = get_object_or_404(JobCard, pk=pk)
        serializer = JobCardSerializer(card, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_job_card(card, serializer.validated_data)
            return Response({"message": "Job card updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        card = get_object_or_404(JobCard, pk=pk)
        services.delete_job_card(card)
        return Response({"message": "Job card deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PRODUCTION TRACKING VIEWSET
# ===========================================================================

class ProductionTrackingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        tracking = services.get_all_production_tracking()
        serializer = ProductionTrackingSerializer(tracking, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        track = get_object_or_404(ProductionTracking, pk=pk)
        serializer = ProductionTrackingSerializer(track)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductionTrackingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_production_tracking(serializer.validated_data)
            return Response({"message": "Production tracking created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        track = get_object_or_404(ProductionTracking, pk=pk)
        serializer = ProductionTrackingSerializer(track, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_production_tracking(track, serializer.validated_data)
            return Response({"message": "Production tracking updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        track = get_object_or_404(ProductionTracking, pk=pk)
        serializer = ProductionTrackingSerializer(track, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_production_tracking(track, serializer.validated_data)
            return Response({"message": "Production tracking updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        track = get_object_or_404(ProductionTracking, pk=pk)
        services.delete_production_tracking(track)
        return Response({"message": "Production tracking deleted successfully."}, status=status.HTTP_200_OK)
