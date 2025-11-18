from decimal import Decimal
from enum import Enum
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from enumfields import EnumField

User = get_user_model()


class MeasurementUnit(Enum):
    GRAM = "g"
    KILOGRAM = "kg"
    TONNE = "tonne"
    MILLILITER = "ml"
    LITER = "l"
    PIECE = "piece"
    DOZEN = "dozen"
    BUNCH = "bunch"
    PACKET = "packet"
    SACK = "sack"
    CRATE = "crate"
    TRAY = "tray"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    stock = models.DecimalField(decimal_places=3, max_digits=13, default=Decimal("0.000"))
    unit = EnumField(MeasurementUnit, default=MeasurementUnit.KILOGRAM, max_length=64)
    min_order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    description = models.TextField()
    image = models.ImageField(upload_to="products")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name", "category"])
        ]
