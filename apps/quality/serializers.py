from rest_framework import serializers
from .models import (
    QualityCheck, DefectCategory, Inspection, InspectionChecklistItem,
    InspectionMeasurement, InspectionDefect, NCRRecord, CAPARecord, ReworkRecord,
)


# ===========================================================================
# QUALITY CHECK SERIALIZER
# ===========================================================================

class QualityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityCheck
        fields = '__all__'


# ===========================================================================
# DEFECT CATEGORY SERIALIZER
# ===========================================================================

class DefectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectCategory
        fields = '__all__'


# ===========================================================================
# INSPECTION CHECKLIST ITEM SERIALIZER
# ===========================================================================

class InspectionChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionChecklistItem
        fields = '__all__'
        extra_kwargs = {'inspection': {'required': False}}


# ===========================================================================
# INSPECTION MEASUREMENT SERIALIZER
# ===========================================================================

class InspectionMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionMeasurement
        fields = '__all__'
        extra_kwargs = {'inspection': {'required': False}}


# ===========================================================================
# INSPECTION DEFECT SERIALIZER
# ===========================================================================

class InspectionDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionDefect
        fields = '__all__'
        extra_kwargs = {'inspection': {'required': False}}


# ===========================================================================
# INSPECTION SERIALIZER
# ===========================================================================

class InspectionSerializer(serializers.ModelSerializer):
    checklist_items = InspectionChecklistItemSerializer(many=True, required=False)
    measurements = InspectionMeasurementSerializer(many=True, required=False)
    defects = InspectionDefectSerializer(many=True, required=False)

    class Meta:
        model = Inspection
        fields = '__all__'


# ===========================================================================
# NCR RECORD SERIALIZER
# ===========================================================================

class NCRRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCRRecord
        fields = '__all__'


# ===========================================================================
# CAPA RECORD SERIALIZER
# ===========================================================================

class CAPARecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CAPARecord
        fields = '__all__'


# ===========================================================================
# REWORK RECORD SERIALIZER
# ===========================================================================

class ReworkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReworkRecord
        fields = '__all__'
