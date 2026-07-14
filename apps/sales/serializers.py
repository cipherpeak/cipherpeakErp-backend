from rest_framework import serializers
from .models import (
    Customer, PriceList, PriceListItem, SalesOrder, SOLine, Delivery, DeliveryLine,
    SalesInvoice, SalesInvoiceLine, SalesReturn, SalesReturnLine, CustomerPayment,
)


# ===========================================================================
# CUSTOMER SERIALIZER
# ===========================================================================

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# ===========================================================================
# PRICE LIST SERIALIZERS
# ===========================================================================

class PriceListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListItem
        fields = '__all__'
        extra_kwargs = {'price_list': {'required': False}}


class PriceListSerializer(serializers.ModelSerializer):
    items = PriceListItemSerializer(many=True, required=False)

    class Meta:
        model = PriceList
        fields = '__all__'


# ===========================================================================
# SALES ORDER SERIALIZERS
# ===========================================================================

class SOLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOLine
        fields = '__all__'
        extra_kwargs = {'sales_order': {'required': False}}


class SalesOrderSerializer(serializers.ModelSerializer):
    lines = SOLineSerializer(many=True, required=False)

    class Meta:
        model = SalesOrder
        fields = '__all__'


# ===========================================================================
# DELIVERY SERIALIZERS
# ===========================================================================

class DeliveryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLine
        fields = '__all__'
        extra_kwargs = {'delivery': {'required': False}}


class DeliverySerializer(serializers.ModelSerializer):
    lines = DeliveryLineSerializer(many=True, required=False)

    class Meta:
        model = Delivery
        fields = '__all__'


# ===========================================================================
# SALES INVOICE SERIALIZERS
# ===========================================================================

class SalesInvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceLine
        fields = '__all__'
        extra_kwargs = {'invoice': {'required': False}}


class SalesInvoiceSerializer(serializers.ModelSerializer):
    lines = SalesInvoiceLineSerializer(many=True, required=False)

    class Meta:
        model = SalesInvoice
        fields = '__all__'


# ===========================================================================
# SALES RETURN SERIALIZERS
# ===========================================================================

class SalesReturnLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturnLine
        fields = '__all__'
        extra_kwargs = {'sales_return': {'required': False}}


class SalesReturnSerializer(serializers.ModelSerializer):
    lines = SalesReturnLineSerializer(many=True, required=False)

    class Meta:
        model = SalesReturn
        fields = '__all__'


# ===========================================================================
# CUSTOMER PAYMENT SERIALIZER
# ===========================================================================

class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPayment
        fields = '__all__'
