from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    VendorCategory, PaymentTerm, Vendor, VendorContact,
    PurchaseRequest, PurchaseRequestItem, RFQ, RFQVendor, RFQItem,
    Quotation, QuotationItem, PurchaseOrder, PurchaseOrderItem,
    GRN, GRNItem, PurchaseInvoice, PurchaseInvoiceItem, VendorPayment,
)
from .serializers import (
    VendorCategorySerializer, PaymentTermSerializer, VendorSerializer, VendorContactSerializer,
    PurchaseRequestSerializer, PurchaseRequestItemSerializer,
    RFQSerializer, RFQVendorSerializer, RFQItemSerializer,
    QuotationSerializer, QuotationItemSerializer,
    PurchaseOrderSerializer, PurchaseOrderItemSerializer,
    GRNSerializer, GRNItemSerializer,
    PurchaseInvoiceSerializer, PurchaseInvoiceItemSerializer,
    VendorPaymentSerializer,
)
from . import services


# ===========================================================================
# VENDOR CATEGORY VIEWSET
# ===========================================================================

class VendorCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories = services.get_all_vendor_categories()
        serializer = VendorCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(VendorCategory, pk=pk)
        serializer = VendorCategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = VendorCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_vendor_category(serializer.validated_data)
            return Response({"message": "Vendor category created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = get_object_or_404(VendorCategory, pk=pk)
        serializer = VendorCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor_category(category, serializer.validated_data)
            return Response({"message": "Vendor category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        category = get_object_or_404(VendorCategory, pk=pk)
        serializer = VendorCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor_category(category, serializer.validated_data)
            return Response({"message": "Vendor category updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = get_object_or_404(VendorCategory, pk=pk)
        services.delete_vendor_category(category)
        return Response({"message": "Vendor category deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PAYMENT TERMS VIEWSET
# ===========================================================================

class PaymentTermViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        terms = services.get_all_payment_terms()
        serializer = PaymentTermSerializer(terms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        term = get_object_or_404(PaymentTerm, pk=pk)
        serializer = PaymentTermSerializer(term)
        return Response(serializer.data)

    def create(self, request):
        serializer = PaymentTermSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_payment_term(serializer.validated_data)
            return Response({"message": "Payment term created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        term = get_object_or_404(PaymentTerm, pk=pk)
        serializer = PaymentTermSerializer(term, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_payment_term(term, serializer.validated_data)
            return Response({"message": "Payment term updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        term = get_object_or_404(PaymentTerm, pk=pk)
        serializer = PaymentTermSerializer(term, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_payment_term(term, serializer.validated_data)
            return Response({"message": "Payment term updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        term = get_object_or_404(PaymentTerm, pk=pk)
        services.delete_payment_term(term)
        return Response({"message": "Payment term deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# VENDOR VIEWSET
# ===========================================================================

class VendorViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        vendors = services.get_all_vendors()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def create(self, request):
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_vendor(serializer.validated_data)
            return Response({"message": "Vendor created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor(vendor, serializer.validated_data)
            return Response({"message": "Vendor updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor(vendor, serializer.validated_data)
            return Response({"message": "Vendor updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        vendor = get_object_or_404(Vendor, pk=pk)
        services.delete_vendor(vendor)
        return Response({"message": "Vendor deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# VENDOR CONTACT VIEWSET
# ===========================================================================

class VendorContactViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            contacts = services.get_vendor_contacts(int(vendor_id))
        else:
            contacts = VendorContact.objects.all()
        serializer = VendorContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = VendorContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_vendor_contact(serializer.validated_data)
            return Response({"message": "Contact created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        contact = get_object_or_404(VendorContact, pk=pk)
        serializer = VendorContactSerializer(contact, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor_contact(contact, serializer.validated_data)
            return Response({"message": "Contact updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contact = get_object_or_404(VendorContact, pk=pk)
        services.delete_vendor_contact(contact)
        return Response({"message": "Contact deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PURCHASE REQUEST VIEWSET
# ===========================================================================

class PurchaseRequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        prs = services.get_all_purchase_requests()
        serializer = PurchaseRequestSerializer(prs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pr = services.get_purchase_request_with_items(pk)
        serializer = PurchaseRequestSerializer(pr)
        return Response(serializer.data)

    def create(self, request):
        serializer = PurchaseRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_purchase_request(serializer.validated_data)
            return Response({"message": "Purchase request created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        pr = get_object_or_404(PurchaseRequest, pk=pk)
        serializer = PurchaseRequestSerializer(pr, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_purchase_request(pr, serializer.validated_data)
            return Response({"message": "Purchase request updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pr = get_object_or_404(PurchaseRequest, pk=pk)
        serializer = PurchaseRequestSerializer(pr, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_purchase_request(pr, serializer.validated_data)
            return Response({"message": "Purchase request updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        pr = get_object_or_404(PurchaseRequest, pk=pk)
        services.delete_purchase_request(pr)
        return Response({"message": "Purchase request deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# RFQ VIEWSET
# ===========================================================================

class RFQViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        rfqs = services.get_all_rfqs()
        serializer = RFQSerializer(rfqs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        rfq = services.get_rfq_with_details(pk)
        serializer = RFQSerializer(rfq)
        return Response(serializer.data)

    def create(self, request):
        serializer = RFQSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_rfq(serializer.validated_data)
            return Response({"message": "RFQ created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        rfq = get_object_or_404(RFQ, pk=pk)
        serializer = RFQSerializer(rfq, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_rfq(rfq, serializer.validated_data)
            return Response({"message": "RFQ updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        rfq = get_object_or_404(RFQ, pk=pk)
        serializer = RFQSerializer(rfq, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_rfq(rfq, serializer.validated_data)
            return Response({"message": "RFQ updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rfq = get_object_or_404(RFQ, pk=pk)
        services.delete_rfq(rfq)
        return Response({"message": "RFQ deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# QUOTATION VIEWSET
# ===========================================================================

class QuotationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        quotations = services.get_all_quotations()
        serializer = QuotationSerializer(quotations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        quotation = services.get_quotation_with_items(pk)
        serializer = QuotationSerializer(quotation)
        return Response(serializer.data)

    def create(self, request):
        serializer = QuotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_quotation(serializer.validated_data)
            return Response({"message": "Quotation created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        quotation = get_object_or_404(Quotation, pk=pk)
        serializer = QuotationSerializer(quotation, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_quotation(quotation, serializer.validated_data)
            return Response({"message": "Quotation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        quotation = get_object_or_404(Quotation, pk=pk)
        serializer = QuotationSerializer(quotation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_quotation(quotation, serializer.validated_data)
            return Response({"message": "Quotation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        quotation = get_object_or_404(Quotation, pk=pk)
        services.delete_quotation(quotation)
        return Response({"message": "Quotation deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PURCHASE ORDER VIEWSET
# ===========================================================================

class PurchaseOrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        pos = services.get_all_purchase_orders()
        serializer = PurchaseOrderSerializer(pos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        po = services.get_purchase_order_with_items(pk)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data)

    def create(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_purchase_order(serializer.validated_data)
            return Response({"message": "Purchase order created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        serializer = PurchaseOrderSerializer(po, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_purchase_order(po, serializer.validated_data)
            return Response({"message": "Purchase order updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        serializer = PurchaseOrderSerializer(po, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_purchase_order(po, serializer.validated_data)
            return Response({"message": "Purchase order updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        services.delete_purchase_order(po)
        return Response({"message": "Purchase order deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# GRN VIEWSET
# ===========================================================================

class GRNViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        grns = services.get_all_grns()
        serializer = GRNSerializer(grns, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        grn = services.get_grn_with_items(pk)
        serializer = GRNSerializer(grn)
        return Response(serializer.data)

    def create(self, request):
        serializer = GRNSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_grn(serializer.validated_data)
            return Response({"message": "GRN created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        grn = get_object_or_404(GRN, pk=pk)
        serializer = GRNSerializer(grn, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_grn(grn, serializer.validated_data)
            return Response({"message": "GRN updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        grn = get_object_or_404(GRN, pk=pk)
        serializer = GRNSerializer(grn, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_grn(grn, serializer.validated_data)
            return Response({"message": "GRN updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        grn = get_object_or_404(GRN, pk=pk)
        services.delete_grn(grn)
        return Response({"message": "GRN deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PURCHASE INVOICE VIEWSET
# ===========================================================================

class PurchaseInvoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        invoices = services.get_all_purchase_invoices()
        serializer = PurchaseInvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        invoice = services.get_purchase_invoice_with_items(pk)
        serializer = PurchaseInvoiceSerializer(invoice)
        return Response(serializer.data)

    def create(self, request):
        serializer = PurchaseInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_purchase_invoice(serializer.validated_data)
            return Response({"message": "Invoice created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        invoice = get_object_or_404(PurchaseInvoice, pk=pk)
        serializer = PurchaseInvoiceSerializer(invoice, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_purchase_invoice(invoice, serializer.validated_data)
            return Response({"message": "Invoice updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        invoice = get_object_or_404(PurchaseInvoice, pk=pk)
        serializer = PurchaseInvoiceSerializer(invoice, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_purchase_invoice(invoice, serializer.validated_data)
            return Response({"message": "Invoice updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        invoice = get_object_or_404(PurchaseInvoice, pk=pk)
        services.delete_purchase_invoice(invoice)
        return Response({"message": "Invoice deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# VENDOR PAYMENT VIEWSET
# ===========================================================================

class VendorPaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        payments = services.get_all_vendor_payments()
        serializer = VendorPaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        payment = get_object_or_404(VendorPayment, pk=pk)
        serializer = VendorPaymentSerializer(payment)
        return Response(serializer.data)

    def create(self, request):
        serializer = VendorPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_vendor_payment(serializer.validated_data)
            return Response({"message": "Payment created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        payment = get_object_or_404(VendorPayment, pk=pk)
        serializer = VendorPaymentSerializer(payment, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor_payment(payment, serializer.validated_data)
            return Response({"message": "Payment updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        payment = get_object_or_404(VendorPayment, pk=pk)
        serializer = VendorPaymentSerializer(payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_vendor_payment(payment, serializer.validated_data)
            return Response({"message": "Payment updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        payment = get_object_or_404(VendorPayment, pk=pk)
        services.delete_vendor_payment(payment)
        return Response({"message": "Payment deleted successfully."}, status=status.HTTP_200_OK)
