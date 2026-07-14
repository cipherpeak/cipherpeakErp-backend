from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    QualityCheck, DefectCategory, Inspection, NCRRecord, CAPARecord, ReworkRecord,
)
from .serializers import (
    QualityCheckSerializer, DefectCategorySerializer, InspectionSerializer,
    NCRRecordSerializer, CAPARecordSerializer, ReworkRecordSerializer,
)
from . import services


# ===========================================================================
# QUALITY CHECK VIEWSET
# ===========================================================================

class QualityCheckViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        checks = services.get_all_quality_checks()
        serializer = QualityCheckSerializer(checks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        check = get_object_or_404(QualityCheck, pk=pk)
        serializer = QualityCheckSerializer(check)
        return Response(serializer.data)

    def create(self, request):
        serializer = QualityCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_quality_check(serializer.validated_data)
            return Response({"message": "Quality check created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        check = get_object_or_404(QualityCheck, pk=pk)
        serializer = QualityCheckSerializer(check, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_quality_check(check, serializer.validated_data)
            return Response({"message": "Quality check updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        check = get_object_or_404(QualityCheck, pk=pk)
        serializer = QualityCheckSerializer(check, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_quality_check(check, serializer.validated_data)
            return Response({"message": "Quality check updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        check = get_object_or_404(QualityCheck, pk=pk)
        services.delete_quality_check(check)
        return Response({"message": "Quality check deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# DEFECT CATEGORY VIEWSET
# ===========================================================================

class DefectCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories = services.get_all_defect_categories()
        serializer = DefectCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(DefectCategory, pk=pk)
        serializer = DefectCategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = DefectCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_defect_category(serializer.validated_data)
            return Response({"message": "Defect category created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = get_object_or_404(DefectCategory, pk=pk)
        serializer = DefectCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_defect_category(category, serializer.validated_data)
            return Response({"message": "Defect category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = get_object_or_404(DefectCategory, pk=pk)
        serializer = DefectCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_defect_category(category, serializer.validated_data)
            return Response({"message": "Defect category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = get_object_or_404(DefectCategory, pk=pk)
        services.delete_defect_category(category)
        return Response({"message": "Defect category deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# INSPECTION VIEWSET
# ===========================================================================

class InspectionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        inspections = services.get_all_inspections()
        serializer = InspectionSerializer(inspections, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        inspection = services.get_inspection_with_details(pk)
        serializer = InspectionSerializer(inspection)
        return Response(serializer.data)

    def create(self, request):
        serializer = InspectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_inspection(serializer.validated_data)
            return Response({"message": "Inspection created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        inspection = get_object_or_404(Inspection, pk=pk)
        serializer = InspectionSerializer(inspection, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_inspection(inspection, serializer.validated_data)
            return Response({"message": "Inspection updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        inspection = get_object_or_404(Inspection, pk=pk)
        serializer = InspectionSerializer(inspection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_inspection(inspection, serializer.validated_data)
            return Response({"message": "Inspection updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        inspection = get_object_or_404(Inspection, pk=pk)
        services.delete_inspection(inspection)
        return Response({"message": "Inspection deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# NCR RECORD VIEWSET
# ===========================================================================

class NCRRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        records = services.get_all_ncr_records()
        serializer = NCRRecordSerializer(records, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        record = get_object_or_404(NCRRecord, pk=pk)
        serializer = NCRRecordSerializer(record)
        return Response(serializer.data)

    def create(self, request):
        serializer = NCRRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_ncr_record(serializer.validated_data)
            return Response({"message": "NCR record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        record = get_object_or_404(NCRRecord, pk=pk)
        serializer = NCRRecordSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_ncr_record(record, serializer.validated_data)
            return Response({"message": "NCR record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        record = get_object_or_404(NCRRecord, pk=pk)
        serializer = NCRRecordSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_ncr_record(record, serializer.validated_data)
            return Response({"message": "NCR record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        record = get_object_or_404(NCRRecord, pk=pk)
        services.delete_ncr_record(record)
        return Response({"message": "NCR record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CAPA RECORD VIEWSET
# ===========================================================================

class CAPARecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        records = services.get_all_capa_records()
        serializer = CAPARecordSerializer(records, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        record = get_object_or_404(CAPARecord, pk=pk)
        serializer = CAPARecordSerializer(record)
        return Response(serializer.data)

    def create(self, request):
        serializer = CAPARecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_capa_record(serializer.validated_data)
            return Response({"message": "CAPA record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        record = get_object_or_404(CAPARecord, pk=pk)
        serializer = CAPARecordSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_capa_record(record, serializer.validated_data)
            return Response({"message": "CAPA record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        record = get_object_or_404(CAPARecord, pk=pk)
        serializer = CAPARecordSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_capa_record(record, serializer.validated_data)
            return Response({"message": "CAPA record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        record = get_object_or_404(CAPARecord, pk=pk)
        services.delete_capa_record(record)
        return Response({"message": "CAPA record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# REWORK RECORD VIEWSET
# ===========================================================================

class ReworkRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        records = services.get_all_rework_records()
        serializer = ReworkRecordSerializer(records, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        record = get_object_or_404(ReworkRecord, pk=pk)
        serializer = ReworkRecordSerializer(record)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReworkRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_rework_record(serializer.validated_data)
            return Response({"message": "Rework record created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        record = get_object_or_404(ReworkRecord, pk=pk)
        serializer = ReworkRecordSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_rework_record(record, serializer.validated_data)
            return Response({"message": "Rework record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        record = get_object_or_404(ReworkRecord, pk=pk)
        serializer = ReworkRecordSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_rework_record(record, serializer.validated_data)
            return Response({"message": "Rework record updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        record = get_object_or_404(ReworkRecord, pk=pk)
        services.delete_rework_record(record)
        return Response({"message": "Rework record deleted successfully."}, status=status.HTTP_200_OK)
