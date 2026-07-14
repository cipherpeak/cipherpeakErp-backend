from rest_framework import serializers
from .models import (
    MachineCategory, Machine, ProductionLine, WorkCenter, Product,
    BOMCategory, BillOfMaterial, BOMMaterial, BOMOperation, BOMVersion, BOMSubstitution,
    ProductionPlan, ProductionPlanMaterial, WorkOrder, WorkOrderMaterial,
    WorkOrderOperation, WorkOrderQualityCheck, JobCard, ProductionTracking,
)


# ===========================================================================
# MACHINE CATEGORY SERIALIZER
# ===========================================================================

class MachineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCategory
        fields = '__all__'


# ===========================================================================
# MACHINE SERIALIZER
# ===========================================================================

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


# ===========================================================================
# PRODUCTION LINE SERIALIZER
# ===========================================================================

class ProductionLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionLine
        fields = '__all__'


# ===========================================================================
# WORK CENTER SERIALIZER
# ===========================================================================

class WorkCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCenter
        fields = '__all__'


# ===========================================================================
# PRODUCT SERIALIZER
# ===========================================================================

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ===========================================================================
# BOM CATEGORY SERIALIZER
# ===========================================================================

class BOMCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMCategory
        fields = '__all__'


# ===========================================================================
# BOM MATERIAL SERIALIZER
# ===========================================================================

class BOMMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMMaterial
        fields = '__all__'


# ===========================================================================
# BOM OPERATION SERIALIZER
# ===========================================================================

class BOMOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMOperation
        fields = '__all__'


# ===========================================================================
# BOM VERSION SERIALIZER
# ===========================================================================

class BOMVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMVersion
        fields = '__all__'


# ===========================================================================
# BOM SUBSTITUTION SERIALIZER
# ===========================================================================

class BOMSubstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMSubstitution
        fields = '__all__'


# ===========================================================================
# BILL OF MATERIALS SERIALIZER
# ===========================================================================

class BillOfMaterialSerializer(serializers.ModelSerializer):
    bom_materials = BOMMaterialSerializer(many=True, read_only=True)
    bom_operations = BOMOperationSerializer(many=True, read_only=True)

    class Meta:
        model = BillOfMaterial
        fields = '__all__'


# ===========================================================================
# PRODUCTION PLAN MATERIAL SERIALIZER
# ===========================================================================

class ProductionPlanMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionPlanMaterial
        fields = '__all__'


# ===========================================================================
# PRODUCTION PLAN SERIALIZER
# ===========================================================================

class ProductionPlanSerializer(serializers.ModelSerializer):
    plan_materials = ProductionPlanMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductionPlan
        fields = '__all__'


# ===========================================================================
# WORK ORDER MATERIAL SERIALIZER
# ===========================================================================

class WorkOrderMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderMaterial
        fields = '__all__'


# ===========================================================================
# WORK ORDER OPERATION SERIALIZER
# ===========================================================================

class WorkOrderOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderOperation
        fields = '__all__'


# ===========================================================================
# WORK ORDER QUALITY CHECK SERIALIZER
# ===========================================================================

class WorkOrderQualityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderQualityCheck
        fields = '__all__'


# ===========================================================================
# WORK ORDER SERIALIZER
# ===========================================================================

class WorkOrderSerializer(serializers.ModelSerializer):
    wo_materials = WorkOrderMaterialSerializer(many=True, read_only=True)
    wo_operations = WorkOrderOperationSerializer(many=True, read_only=True)
    quality_checks = WorkOrderQualityCheckSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOrder
        fields = '__all__'


# ===========================================================================
# JOB CARD SERIALIZER
# ===========================================================================

class JobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = '__all__'


# ===========================================================================
# PRODUCTION TRACKING SERIALIZER
# ===========================================================================

class ProductionTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionTracking
        fields = '__all__'
