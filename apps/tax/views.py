from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    TaxJurisdiction, TaxType, HSNCode, TaxRate, TaxCategory,
    TaxGroup, TaxRule, TaxExemption, ReverseChargeRecord, TaxReturn, TaxMappingRule,
)
from .serializers import (
    TaxJurisdictionSerializer, TaxTypeSerializer, HSNCodeSerializer, TaxRateSerializer,
    TaxCategorySerializer, TaxGroupSerializer, TaxRuleSerializer, TaxExemptionSerializer,
    ReverseChargeRecordSerializer, TaxReturnSerializer, TaxMappingRuleSerializer,
)
from . import services


# ===========================================================================
# TAX JURISDICTION VIEWSET
# ===========================================================================

class TaxJurisdictionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxJurisdictionSerializer(services.get_all_jurisdictions(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxJurisdictionSerializer(get_object_or_404(TaxJurisdiction, pk=pk)).data)

    def create(self, request):
        serializer = TaxJurisdictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_jurisdiction(serializer.validated_data)
        return Response({"message": "Tax jurisdiction created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        jurisdiction = get_object_or_404(TaxJurisdiction, pk=pk)
        serializer = TaxJurisdictionSerializer(jurisdiction, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_jurisdiction(jurisdiction, serializer.validated_data)
        return Response({"message": "Tax jurisdiction updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        jurisdiction = get_object_or_404(TaxJurisdiction, pk=pk)
        serializer = TaxJurisdictionSerializer(jurisdiction, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_jurisdiction(jurisdiction, serializer.validated_data)
        return Response({"message": "Tax jurisdiction updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_jurisdiction(get_object_or_404(TaxJurisdiction, pk=pk))
        return Response({"message": "Tax jurisdiction deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX TYPE VIEWSET
# ===========================================================================

class TaxTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxTypeSerializer(services.get_all_tax_types(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxTypeSerializer(get_object_or_404(TaxType, pk=pk)).data)

    def create(self, request):
        serializer = TaxTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_tax_type(serializer.validated_data)
            return Response({"message": "Tax type created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        tax_type = get_object_or_404(TaxType, pk=pk)
        serializer = TaxTypeSerializer(tax_type, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_type(tax_type, serializer.validated_data)
            return Response({"message": "Tax type updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        tax_type = get_object_or_404(TaxType, pk=pk)
        serializer = TaxTypeSerializer(tax_type, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_type(tax_type, serializer.validated_data)
            return Response({"message": "Tax type updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_tax_type(get_object_or_404(TaxType, pk=pk))
        return Response({"message": "Tax type deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# HSN CODE VIEWSET
# ===========================================================================

class HSNCodeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(HSNCodeSerializer(services.get_all_hsn_codes(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(HSNCodeSerializer(get_object_or_404(HSNCode, pk=pk)).data)

    def create(self, request):
        serializer = HSNCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_hsn_code(serializer.validated_data)
            return Response({"message": "HSN code created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        hsn = get_object_or_404(HSNCode, pk=pk)
        serializer = HSNCodeSerializer(hsn, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_hsn_code(hsn, serializer.validated_data)
            return Response({"message": "HSN code updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        hsn = get_object_or_404(HSNCode, pk=pk)
        serializer = HSNCodeSerializer(hsn, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_hsn_code(hsn, serializer.validated_data)
            return Response({"message": "HSN code updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_hsn_code(get_object_or_404(HSNCode, pk=pk))
        return Response({"message": "HSN code deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX RATE VIEWSET
# ===========================================================================

class TaxRateViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxRateSerializer(services.get_all_tax_rates(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxRateSerializer(get_object_or_404(TaxRate, pk=pk)).data)

    def create(self, request):
        serializer = TaxRateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_tax_rate(serializer.validated_data)
            return Response({"message": "Tax rate created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        rate = get_object_or_404(TaxRate, pk=pk)
        serializer = TaxRateSerializer(rate, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_rate(rate, serializer.validated_data)
            return Response({"message": "Tax rate updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        rate = get_object_or_404(TaxRate, pk=pk)
        serializer = TaxRateSerializer(rate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_rate(rate, serializer.validated_data)
            return Response({"message": "Tax rate updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_tax_rate(get_object_or_404(TaxRate, pk=pk))
        return Response({"message": "Tax rate deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX CATEGORY VIEWSET
# ===========================================================================

class TaxCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxCategorySerializer(services.get_all_tax_categories(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxCategorySerializer(get_object_or_404(TaxCategory, pk=pk)).data)

    def create(self, request):
        serializer = TaxCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_tax_category(serializer.validated_data)
        return Response({"message": "Tax category created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        category = get_object_or_404(TaxCategory, pk=pk)
        serializer = TaxCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_tax_category(category, serializer.validated_data)
        return Response({"message": "Tax category updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        category = get_object_or_404(TaxCategory, pk=pk)
        serializer = TaxCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_tax_category(category, serializer.validated_data)
        return Response({"message": "Tax category updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_tax_category(get_object_or_404(TaxCategory, pk=pk))
        return Response({"message": "Tax category deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX GROUP VIEWSET
# ===========================================================================

class TaxGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxGroupSerializer(services.get_all_tax_groups(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxGroupSerializer(services.get_tax_group_with_members(pk)).data)

    def create(self, request):
        serializer = TaxGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_tax_group(serializer.validated_data)
            return Response({"message": "Tax group created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        group = get_object_or_404(TaxGroup, pk=pk)
        serializer = TaxGroupSerializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_group(group, serializer.validated_data)
            return Response({"message": "Tax group updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        group = get_object_or_404(TaxGroup, pk=pk)
        serializer = TaxGroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_group(group, serializer.validated_data)
            return Response({"message": "Tax group updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_tax_group(get_object_or_404(TaxGroup, pk=pk))
        return Response({"message": "Tax group deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX RULE VIEWSET
# ===========================================================================

class TaxRuleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxRuleSerializer(services.get_all_tax_rules(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxRuleSerializer(services.get_tax_rule_with_conditions(pk)).data)

    def create(self, request):
        serializer = TaxRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_tax_rule(serializer.validated_data)
            return Response({"message": "Tax rule created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        rule = get_object_or_404(TaxRule, pk=pk)
        serializer = TaxRuleSerializer(rule, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_rule(rule, serializer.validated_data)
            return Response({"message": "Tax rule updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        rule = get_object_or_404(TaxRule, pk=pk)
        serializer = TaxRuleSerializer(rule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_tax_rule(rule, serializer.validated_data)
            return Response({"message": "Tax rule updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_tax_rule(get_object_or_404(TaxRule, pk=pk))
        return Response({"message": "Tax rule deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX EXEMPTION VIEWSET
# ===========================================================================

class TaxExemptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxExemptionSerializer(services.get_all_exemptions(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxExemptionSerializer(get_object_or_404(TaxExemption, pk=pk)).data)

    def create(self, request):
        serializer = TaxExemptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_exemption(serializer.validated_data)
            return Response({"message": "Tax exemption created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        exemption = get_object_or_404(TaxExemption, pk=pk)
        serializer = TaxExemptionSerializer(exemption, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_exemption(exemption, serializer.validated_data)
            return Response({"message": "Tax exemption updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        exemption = get_object_or_404(TaxExemption, pk=pk)
        serializer = TaxExemptionSerializer(exemption, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_exemption(exemption, serializer.validated_data)
            return Response({"message": "Tax exemption updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        services.delete_exemption(get_object_or_404(TaxExemption, pk=pk))
        return Response({"message": "Tax exemption deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# REVERSE CHARGE RECORD VIEWSET
# ===========================================================================

class ReverseChargeRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(ReverseChargeRecordSerializer(services.get_all_reverse_charge_records(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(ReverseChargeRecordSerializer(get_object_or_404(ReverseChargeRecord, pk=pk)).data)

    def create(self, request):
        serializer = ReverseChargeRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_reverse_charge_record(serializer.validated_data)
        return Response({"message": "Reverse charge record created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        record = get_object_or_404(ReverseChargeRecord, pk=pk)
        serializer = ReverseChargeRecordSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_reverse_charge_record(record, serializer.validated_data)
        return Response({"message": "Reverse charge record updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        record = get_object_or_404(ReverseChargeRecord, pk=pk)
        serializer = ReverseChargeRecordSerializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_reverse_charge_record(record, serializer.validated_data)
        return Response({"message": "Reverse charge record updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_reverse_charge_record(get_object_or_404(ReverseChargeRecord, pk=pk))
        return Response({"message": "Reverse charge record deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX RETURN VIEWSET
# ===========================================================================

class TaxReturnViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxReturnSerializer(services.get_all_tax_returns(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxReturnSerializer(get_object_or_404(TaxReturn, pk=pk)).data)

    def create(self, request):
        serializer = TaxReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_tax_return(serializer.validated_data)
        return Response({"message": "Tax return created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        tax_return = get_object_or_404(TaxReturn, pk=pk)
        serializer = TaxReturnSerializer(tax_return, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_tax_return(tax_return, serializer.validated_data)
        return Response({"message": "Tax return updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        tax_return = get_object_or_404(TaxReturn, pk=pk)
        serializer = TaxReturnSerializer(tax_return, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_tax_return(tax_return, serializer.validated_data)
        return Response({"message": "Tax return updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_tax_return(get_object_or_404(TaxReturn, pk=pk))
        return Response({"message": "Tax return deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TAX MAPPING RULE VIEWSET
# ===========================================================================

class TaxMappingRuleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(TaxMappingRuleSerializer(services.get_all_mapping_rules(), many=True).data)

    def retrieve(self, request, pk=None):
        return Response(TaxMappingRuleSerializer(get_object_or_404(TaxMappingRule, pk=pk)).data)

    def create(self, request):
        serializer = TaxMappingRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_mapping_rule(serializer.validated_data)
        return Response({"message": "Tax mapping rule created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        rule = get_object_or_404(TaxMappingRule, pk=pk)
        serializer = TaxMappingRuleSerializer(rule, data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_mapping_rule(rule, serializer.validated_data)
        return Response({"message": "Tax mapping rule updated successfully."}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        rule = get_object_or_404(TaxMappingRule, pk=pk)
        serializer = TaxMappingRuleSerializer(rule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        services.update_mapping_rule(rule, serializer.validated_data)
        return Response({"message": "Tax mapping rule updated successfully."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        services.delete_mapping_rule(get_object_or_404(TaxMappingRule, pk=pk))
        return Response({"message": "Tax mapping rule deleted successfully."}, status=status.HTTP_200_OK)
