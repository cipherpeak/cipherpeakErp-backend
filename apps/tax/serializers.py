from rest_framework import serializers
from .models import (
    TaxJurisdiction, TaxType, HSNCode, TaxRate, TaxCategory,
    TaxGroup, TaxGroupMember, TaxRule, TaxRuleCondition,
    TaxExemption, ReverseChargeRecord, TaxReturn, TaxMappingRule,
)


class TaxJurisdictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxJurisdiction
        fields = '__all__'


class TaxTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxType
        fields = '__all__'


class HSNCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSNCode
        fields = '__all__'


class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = '__all__'


class TaxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxCategory
        fields = '__all__'


# --- Tax Group + members ---

class TaxGroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxGroupMember
        fields = '__all__'
        extra_kwargs = {'group': {'required': False}}


class TaxGroupSerializer(serializers.ModelSerializer):
    members = TaxGroupMemberSerializer(many=True, required=False)

    class Meta:
        model = TaxGroup
        fields = '__all__'


# --- Tax Rule + conditions ---

class TaxRuleConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRuleCondition
        fields = '__all__'
        extra_kwargs = {'rule': {'required': False}}


class TaxRuleSerializer(serializers.ModelSerializer):
    conditions = TaxRuleConditionSerializer(many=True, required=False)

    class Meta:
        model = TaxRule
        fields = '__all__'


class TaxExemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxExemption
        fields = '__all__'


class ReverseChargeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReverseChargeRecord
        fields = '__all__'


class TaxReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxReturn
        fields = '__all__'


class TaxMappingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxMappingRule
        fields = '__all__'
