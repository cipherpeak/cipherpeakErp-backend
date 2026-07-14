from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Account, Contact, Lead, Opportunity, CRMActivity, CRMQuotation,
)
from .serializers import (
    AccountSerializer, ContactSerializer, LeadSerializer, OpportunitySerializer,
    CRMActivitySerializer, CRMQuotationSerializer,
)
from . import services


# ===========================================================================
# ACCOUNT VIEWSET
# ===========================================================================

class AccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        accounts = services.get_all_accounts()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def create(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_account(serializer.validated_data)
            return Response({"message": "Account created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_account(account, serializer.validated_data)
            return Response({"message": "Account updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_account(account, serializer.validated_data)
            return Response({"message": "Account updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        account = get_object_or_404(Account, pk=pk)
        services.delete_account(account)
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CONTACT VIEWSET
# ===========================================================================

class ContactViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        contacts = services.get_all_contacts()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_contact(serializer.validated_data)
            return Response({"message": "Contact created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_contact(contact, serializer.validated_data)
            return Response({"message": "Contact updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_contact(contact, serializer.validated_data)
            return Response({"message": "Contact updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        services.delete_contact(contact)
        return Response({"message": "Contact deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# LEAD VIEWSET
# ===========================================================================

class LeadViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        leads = services.get_all_leads()
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead)
        return Response(serializer.data)

    def create(self, request):
        serializer = LeadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_lead(serializer.validated_data)
            return Response({"message": "Lead created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_lead(lead, serializer.validated_data)
            return Response({"message": "Lead updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_lead(lead, serializer.validated_data)
            return Response({"message": "Lead updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        lead = get_object_or_404(Lead, pk=pk)
        services.delete_lead(lead)
        return Response({"message": "Lead deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# OPPORTUNITY VIEWSET
# ===========================================================================

class OpportunityViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        opportunities = services.get_all_opportunities()
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        opp = get_object_or_404(Opportunity, pk=pk)
        serializer = OpportunitySerializer(opp)
        return Response(serializer.data)

    def create(self, request):
        serializer = OpportunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_opportunity(serializer.validated_data)
            return Response({"message": "Opportunity created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        opp = get_object_or_404(Opportunity, pk=pk)
        serializer = OpportunitySerializer(opp, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_opportunity(opp, serializer.validated_data)
            return Response({"message": "Opportunity updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        opp = get_object_or_404(Opportunity, pk=pk)
        serializer = OpportunitySerializer(opp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_opportunity(opp, serializer.validated_data)
            return Response({"message": "Opportunity updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        opp = get_object_or_404(Opportunity, pk=pk)
        services.delete_opportunity(opp)
        return Response({"message": "Opportunity deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CRM ACTIVITY VIEWSET
# ===========================================================================

class CRMActivityViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        activities = services.get_all_activities()
        serializer = CRMActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        activity = get_object_or_404(CRMActivity, pk=pk)
        serializer = CRMActivitySerializer(activity)
        return Response(serializer.data)

    def create(self, request):
        serializer = CRMActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_activity(serializer.validated_data)
            return Response({"message": "Activity created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        activity = get_object_or_404(CRMActivity, pk=pk)
        serializer = CRMActivitySerializer(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_activity(activity, serializer.validated_data)
            return Response({"message": "Activity updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        activity = get_object_or_404(CRMActivity, pk=pk)
        serializer = CRMActivitySerializer(activity, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_activity(activity, serializer.validated_data)
            return Response({"message": "Activity updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        activity = get_object_or_404(CRMActivity, pk=pk)
        services.delete_activity(activity)
        return Response({"message": "Activity deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CRM QUOTATION VIEWSET
# ===========================================================================

class CRMQuotationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        quotations = services.get_all_quotations()
        serializer = CRMQuotationSerializer(quotations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        quotation = services.get_quotation_with_lines(pk)
        serializer = CRMQuotationSerializer(quotation)
        return Response(serializer.data)

    def create(self, request):
        serializer = CRMQuotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_quotation(serializer.validated_data)
            return Response({"message": "Quotation created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        quotation = get_object_or_404(CRMQuotation, pk=pk)
        serializer = CRMQuotationSerializer(quotation, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_quotation(quotation, serializer.validated_data)
            return Response({"message": "Quotation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        quotation = get_object_or_404(CRMQuotation, pk=pk)
        serializer = CRMQuotationSerializer(quotation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_quotation(quotation, serializer.validated_data)
            return Response({"message": "Quotation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        quotation = get_object_or_404(CRMQuotation, pk=pk)
        services.delete_quotation(quotation)
        return Response({"message": "Quotation deleted successfully."}, status=status.HTTP_200_OK)
