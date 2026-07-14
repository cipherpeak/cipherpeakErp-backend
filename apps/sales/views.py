from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Customer, PriceList, SalesOrder, Delivery, SalesInvoice, SalesReturn, CustomerPayment,
)
from .serializers import (
    CustomerSerializer, PriceListSerializer, SalesOrderSerializer, DeliverySerializer,
    SalesInvoiceSerializer, SalesReturnSerializer, CustomerPaymentSerializer,
)
from . import services


# ===========================================================================
# CUSTOMER VIEWSET
# ===========================================================================

class CustomerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customers = services.get_all_customers()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_customer(serializer.validated_data)
            return Response({"message": "Customer created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_customer(customer, serializer.validated_data)
            return Response({"message": "Customer updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_customer(customer, serializer.validated_data)
            return Response({"message": "Customer updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        services.delete_customer(customer)
        return Response({"message": "Customer deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PRICE LIST VIEWSET
# ===========================================================================

class PriceListViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        price_lists = services.get_all_price_lists()
        serializer = PriceListSerializer(price_lists, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        price_list = services.get_price_list_with_items(pk)
        serializer = PriceListSerializer(price_list)
        return Response(serializer.data)

    def create(self, request):
        serializer = PriceListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_price_list(serializer.validated_data)
            return Response({"message": "Price list created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        price_list = get_object_or_404(PriceList, pk=pk)
        serializer = PriceListSerializer(price_list, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_price_list(price_list, serializer.validated_data)
            return Response({"message": "Price list updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        price_list = get_object_or_404(PriceList, pk=pk)
        serializer = PriceListSerializer(price_list, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_price_list(price_list, serializer.validated_data)
            return Response({"message": "Price list updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        price_list = get_object_or_404(PriceList, pk=pk)
        services.delete_price_list(price_list)
        return Response({"message": "Price list deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SALES ORDER VIEWSET
# ===========================================================================

class SalesOrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        orders = services.get_all_sales_orders()
        serializer = SalesOrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = services.get_sales_order_with_lines(pk)
        serializer = SalesOrderSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        serializer = SalesOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_sales_order(serializer.validated_data)
            return Response({"message": "Sales order created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        order = get_object_or_404(SalesOrder, pk=pk)
        serializer = SalesOrderSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_sales_order(order, serializer.validated_data)
            return Response({"message": "Sales order updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(SalesOrder, pk=pk)
        serializer = SalesOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_sales_order(order, serializer.validated_data)
            return Response({"message": "Sales order updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(SalesOrder, pk=pk)
        services.delete_sales_order(order)
        return Response({"message": "Sales order deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# DELIVERY VIEWSET
# ===========================================================================

class DeliveryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        deliveries = services.get_all_deliveries()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        delivery = services.get_delivery_with_lines(pk)
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    def create(self, request):
        serializer = DeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_delivery(serializer.validated_data)
            return Response({"message": "Delivery created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        delivery = get_object_or_404(Delivery, pk=pk)
        serializer = DeliverySerializer(delivery, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_delivery(delivery, serializer.validated_data)
            return Response({"message": "Delivery updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        delivery = get_object_or_404(Delivery, pk=pk)
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_delivery(delivery, serializer.validated_data)
            return Response({"message": "Delivery updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        delivery = get_object_or_404(Delivery, pk=pk)
        services.delete_delivery(delivery)
        return Response({"message": "Delivery deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SALES INVOICE VIEWSET
# ===========================================================================

class SalesInvoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        invoices = services.get_all_sales_invoices()
        serializer = SalesInvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        invoice = services.get_sales_invoice_with_lines(pk)
        serializer = SalesInvoiceSerializer(invoice)
        return Response(serializer.data)

    def create(self, request):
        serializer = SalesInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_sales_invoice(serializer.validated_data)
            return Response({"message": "Sales invoice created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        invoice = get_object_or_404(SalesInvoice, pk=pk)
        serializer = SalesInvoiceSerializer(invoice, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_sales_invoice(invoice, serializer.validated_data)
            return Response({"message": "Sales invoice updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        invoice = get_object_or_404(SalesInvoice, pk=pk)
        serializer = SalesInvoiceSerializer(invoice, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_sales_invoice(invoice, serializer.validated_data)
            return Response({"message": "Sales invoice updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        invoice = get_object_or_404(SalesInvoice, pk=pk)
        services.delete_sales_invoice(invoice)
        return Response({"message": "Sales invoice deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SALES RETURN VIEWSET
# ===========================================================================

class SalesReturnViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        returns = services.get_all_sales_returns()
        serializer = SalesReturnSerializer(returns, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        sales_return = services.get_sales_return_with_lines(pk)
        serializer = SalesReturnSerializer(sales_return)
        return Response(serializer.data)

    def create(self, request):
        serializer = SalesReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_sales_return(serializer.validated_data)
            return Response({"message": "Sales return created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        sales_return = get_object_or_404(SalesReturn, pk=pk)
        serializer = SalesReturnSerializer(sales_return, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_sales_return(sales_return, serializer.validated_data)
            return Response({"message": "Sales return updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        sales_return = get_object_or_404(SalesReturn, pk=pk)
        serializer = SalesReturnSerializer(sales_return, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_sales_return(sales_return, serializer.validated_data)
            return Response({"message": "Sales return updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sales_return = get_object_or_404(SalesReturn, pk=pk)
        services.delete_sales_return(sales_return)
        return Response({"message": "Sales return deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# CUSTOMER PAYMENT VIEWSET
# ===========================================================================

class CustomerPaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        payments = services.get_all_customer_payments()
        serializer = CustomerPaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        payment = get_object_or_404(CustomerPayment, pk=pk)
        serializer = CustomerPaymentSerializer(payment)
        return Response(serializer.data)

    def create(self, request):
        serializer = CustomerPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_customer_payment(serializer.validated_data)
            return Response({"message": "Customer payment created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        payment = get_object_or_404(CustomerPayment, pk=pk)
        serializer = CustomerPaymentSerializer(payment, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_customer_payment(payment, serializer.validated_data)
            return Response({"message": "Customer payment updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        payment = get_object_or_404(CustomerPayment, pk=pk)
        serializer = CustomerPaymentSerializer(payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_customer_payment(payment, serializer.validated_data)
            return Response({"message": "Customer payment updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        payment = get_object_or_404(CustomerPayment, pk=pk)
        services.delete_customer_payment(payment)
        return Response({"message": "Customer payment deleted successfully."}, status=status.HTTP_200_OK)
