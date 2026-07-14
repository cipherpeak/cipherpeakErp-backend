from rest_framework import serializers
from .models import (
    Account, Contact, Lead, Opportunity, CRMActivity, CRMQuotation, CRMQuotationLine,
)


# ===========================================================================
# ACCOUNT SERIALIZER
# ===========================================================================

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


# ===========================================================================
# CONTACT SERIALIZER
# ===========================================================================

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# ===========================================================================
# LEAD SERIALIZER
# ===========================================================================

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


# ===========================================================================
# OPPORTUNITY SERIALIZER
# ===========================================================================

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'


# ===========================================================================
# CRM ACTIVITY SERIALIZER
# ===========================================================================

class CRMActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMActivity
        fields = '__all__'


# ===========================================================================
# CRM QUOTATION LINE SERIALIZER
# ===========================================================================

class CRMQuotationLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMQuotationLine
        fields = '__all__'
        extra_kwargs = {'quotation': {'required': False}}


# ===========================================================================
# CRM QUOTATION SERIALIZER
# ===========================================================================

class CRMQuotationSerializer(serializers.ModelSerializer):
    lines = CRMQuotationLineSerializer(many=True, required=False)

    class Meta:
        model = CRMQuotation
        fields = '__all__'
