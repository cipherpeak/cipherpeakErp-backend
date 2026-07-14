from typing import Dict, Any, List
from .models import (
    Customer, PriceList, PriceListItem, SalesOrder, SOLine, Delivery, DeliveryLine,
    SalesInvoice, SalesInvoiceLine, SalesReturn, SalesReturnLine, CustomerPayment,
)


# ===========================================================================
# CUSTOMER SERVICES
# ===========================================================================

def get_all_customers() -> List[Customer]:
    return Customer.objects.filter(is_deleted=False)

def create_customer(data: Dict[str, Any]) -> Customer:
    customer_number = data.get('customer_number')
    if Customer.objects.filter(customer_number__iexact=customer_number).exists():
        raise ValueError(f"Customer number '{customer_number}' already exists.")
    return Customer.objects.create(**data)

def update_customer(customer: Customer, data: Dict[str, Any]) -> Customer:
    customer_number = data.get('customer_number')
    if customer_number and Customer.objects.filter(
        customer_number__iexact=customer_number,
    ).exclude(id=customer.id).exists():
        raise ValueError(f"Customer number '{customer_number}' already exists.")
    for field, value in data.items():
        setattr(customer, field, value)
    customer.save()
    return customer

def delete_customer(customer: Customer) -> None:
    customer.is_deleted = True
    customer.save()


# ===========================================================================
# PRICE LIST SERVICES
# ===========================================================================

def get_all_price_lists() -> List[PriceList]:
    return PriceList.objects.filter(is_deleted=False)

def get_price_list_with_items(price_list_id: int) -> PriceList:
    return PriceList.objects.prefetch_related('items').get(pk=price_list_id)

def create_price_list(data: Dict[str, Any]) -> PriceList:
    code = data.get('code')
    if PriceList.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Price list code '{code}' already exists.")
    items_data = data.pop('items', [])
    price_list = PriceList.objects.create(**data)
    for item_data in items_data:
        PriceListItem.objects.create(price_list=price_list, **item_data)
    return price_list

def update_price_list(price_list: PriceList, data: Dict[str, Any]) -> PriceList:
    code = data.get('code')
    if code and PriceList.objects.filter(code__iexact=code).exclude(id=price_list.id).exists():
        raise ValueError(f"Price list code '{code}' already exists.")
    data.pop('items', None)
    for field, value in data.items():
        setattr(price_list, field, value)
    price_list.save()
    return price_list

def delete_price_list(price_list: PriceList) -> None:
    price_list.is_deleted = True
    price_list.save()


# ===========================================================================
# SALES ORDER SERVICES
# ===========================================================================

def get_all_sales_orders() -> List[SalesOrder]:
    return SalesOrder.objects.filter(is_deleted=False)

def get_sales_order_with_lines(order_id: int) -> SalesOrder:
    return SalesOrder.objects.prefetch_related('lines').get(pk=order_id)

def create_sales_order(data: Dict[str, Any]) -> SalesOrder:
    order_number = data.get('order_number')
    if SalesOrder.objects.filter(order_number__iexact=order_number).exists():
        raise ValueError(f"Order number '{order_number}' already exists.")
    lines_data = data.pop('lines', [])
    order = SalesOrder.objects.create(**data)
    for line_data in lines_data:
        SOLine.objects.create(sales_order=order, **line_data)
    return order

def update_sales_order(order: SalesOrder, data: Dict[str, Any]) -> SalesOrder:
    order_number = data.get('order_number')
    if order_number and SalesOrder.objects.filter(
        order_number__iexact=order_number,
    ).exclude(id=order.id).exists():
        raise ValueError(f"Order number '{order_number}' already exists.")
    data.pop('lines', None)
    for field, value in data.items():
        setattr(order, field, value)
    order.save()
    return order

def delete_sales_order(order: SalesOrder) -> None:
    order.is_deleted = True
    order.save()


# ===========================================================================
# DELIVERY SERVICES
# ===========================================================================

def get_all_deliveries() -> List[Delivery]:
    return Delivery.objects.filter(is_deleted=False)

def get_delivery_with_lines(delivery_id: int) -> Delivery:
    return Delivery.objects.prefetch_related('lines').get(pk=delivery_id)

def create_delivery(data: Dict[str, Any]) -> Delivery:
    delivery_number = data.get('delivery_number')
    if Delivery.objects.filter(delivery_number__iexact=delivery_number).exists():
        raise ValueError(f"Delivery number '{delivery_number}' already exists.")
    lines_data = data.pop('lines', [])
    delivery = Delivery.objects.create(**data)
    for line_data in lines_data:
        DeliveryLine.objects.create(delivery=delivery, **line_data)
    return delivery

def update_delivery(delivery: Delivery, data: Dict[str, Any]) -> Delivery:
    delivery_number = data.get('delivery_number')
    if delivery_number and Delivery.objects.filter(
        delivery_number__iexact=delivery_number,
    ).exclude(id=delivery.id).exists():
        raise ValueError(f"Delivery number '{delivery_number}' already exists.")
    data.pop('lines', None)
    for field, value in data.items():
        setattr(delivery, field, value)
    delivery.save()
    return delivery

def delete_delivery(delivery: Delivery) -> None:
    delivery.is_deleted = True
    delivery.save()


# ===========================================================================
# SALES INVOICE SERVICES
# ===========================================================================

def get_all_sales_invoices() -> List[SalesInvoice]:
    return SalesInvoice.objects.filter(is_deleted=False)

def get_sales_invoice_with_lines(invoice_id: int) -> SalesInvoice:
    return SalesInvoice.objects.prefetch_related('lines').get(pk=invoice_id)

def create_sales_invoice(data: Dict[str, Any]) -> SalesInvoice:
    invoice_number = data.get('invoice_number')
    if SalesInvoice.objects.filter(invoice_number__iexact=invoice_number).exists():
        raise ValueError(f"Invoice number '{invoice_number}' already exists.")
    lines_data = data.pop('lines', [])
    invoice = SalesInvoice.objects.create(**data)
    for line_data in lines_data:
        SalesInvoiceLine.objects.create(invoice=invoice, **line_data)
    return invoice

def update_sales_invoice(invoice: SalesInvoice, data: Dict[str, Any]) -> SalesInvoice:
    invoice_number = data.get('invoice_number')
    if invoice_number and SalesInvoice.objects.filter(
        invoice_number__iexact=invoice_number,
    ).exclude(id=invoice.id).exists():
        raise ValueError(f"Invoice number '{invoice_number}' already exists.")
    data.pop('lines', None)
    for field, value in data.items():
        setattr(invoice, field, value)
    invoice.save()
    return invoice

def delete_sales_invoice(invoice: SalesInvoice) -> None:
    invoice.is_deleted = True
    invoice.save()


# ===========================================================================
# SALES RETURN SERVICES
# ===========================================================================

def get_all_sales_returns() -> List[SalesReturn]:
    return SalesReturn.objects.filter(is_deleted=False)

def get_sales_return_with_lines(return_id: int) -> SalesReturn:
    return SalesReturn.objects.prefetch_related('lines').get(pk=return_id)

def create_sales_return(data: Dict[str, Any]) -> SalesReturn:
    return_number = data.get('return_number')
    if SalesReturn.objects.filter(return_number__iexact=return_number).exists():
        raise ValueError(f"Return number '{return_number}' already exists.")
    lines_data = data.pop('lines', [])
    sales_return = SalesReturn.objects.create(**data)
    for line_data in lines_data:
        SalesReturnLine.objects.create(sales_return=sales_return, **line_data)
    return sales_return

def update_sales_return(sales_return: SalesReturn, data: Dict[str, Any]) -> SalesReturn:
    return_number = data.get('return_number')
    if return_number and SalesReturn.objects.filter(
        return_number__iexact=return_number,
    ).exclude(id=sales_return.id).exists():
        raise ValueError(f"Return number '{return_number}' already exists.")
    data.pop('lines', None)
    for field, value in data.items():
        setattr(sales_return, field, value)
    sales_return.save()
    return sales_return

def delete_sales_return(sales_return: SalesReturn) -> None:
    sales_return.is_deleted = True
    sales_return.save()


# ===========================================================================
# CUSTOMER PAYMENT SERVICES
# ===========================================================================

def get_all_customer_payments() -> List[CustomerPayment]:
    return CustomerPayment.objects.filter(is_deleted=False)

def create_customer_payment(data: Dict[str, Any]) -> CustomerPayment:
    payment_number = data.get('payment_number')
    if CustomerPayment.objects.filter(payment_number__iexact=payment_number).exists():
        raise ValueError(f"Payment number '{payment_number}' already exists.")
    return CustomerPayment.objects.create(**data)

def update_customer_payment(payment: CustomerPayment, data: Dict[str, Any]) -> CustomerPayment:
    payment_number = data.get('payment_number')
    if payment_number and CustomerPayment.objects.filter(
        payment_number__iexact=payment_number,
    ).exclude(id=payment.id).exists():
        raise ValueError(f"Payment number '{payment_number}' already exists.")
    for field, value in data.items():
        setattr(payment, field, value)
    payment.save()
    return payment

def delete_customer_payment(payment: CustomerPayment) -> None:
    payment.is_deleted = True
    payment.save()
