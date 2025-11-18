from decimal import Decimal
from enum import Enum
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from enumfields import EnumField

from orders.models import Order

User = get_user_model()


class PaymentMethod(Enum):
    CASH = "cash"
    MPESA = "mpesa"
    CARD = "card"


class Payment(models.Model):
    """
    Payments applied to an order. supports partial payments.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    method = EnumField(PaymentMethod, max_length=64)
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.amount} ({self.method.value}) for Order {self.order.id}"
