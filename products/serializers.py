from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import EnumField

from .models import MeasurementUnit, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Product objects
    """
    class _Farmer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "name", "location"]

    
    unit = EnumField(enum_class=MeasurementUnit)
    farmer = _Farmer(source="seller", read_only=True)

    class Meta:
        model = Product
        fields = [ 
            "id", "name", "category", "price", "stock", "unit", "description", "image",
            "farmer", "created_at", "updated_at",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for product creation
    """
    unit = serializers.ChoiceField(choices=[item.value for item in MeasurementUnit])

    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock", "unit", "description", "image"]
    

class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Product objects
    """
    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock", "unit", "description", "image"]
