from decimal import Decimal
from enum import Enum
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from enumfields import EnumField

from products.models import Product

User = get_user_model()


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PACKED = "packed"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Order(models.Model):
    """
    Represents a customer's order which contains multiple OrderItems.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = EnumField(OrderStatus, default=OrderStatus.PENDING, max_length=64)
    payment_status = EnumField(PaymentStatus, default=PaymentStatus.PENDING, max_length=64)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} - {self.buyer}"


class OrderItem(models.Model):
    """
    Individual line item in an order.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sold_items")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    quantity = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal("0.001"))])

    class Meta:
        ordering = ["-created_at"]

    @property
    def item_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product} x {self.quantity}"
