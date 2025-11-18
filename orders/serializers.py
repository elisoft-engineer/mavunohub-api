from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from core.serializers import EnumField

from .models import Order, OrderItem, OrderStatus, PaymentStatus


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderItem
        fields = [
            "product", "unit_price", "quantity", "item_total"
        ]


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=OrderStatus)
    payment_status = EnumField(enum_class=PaymentStatus)
    items = OrderItemSerializer(many=True)
    buyer = serializers.CharField(source="buyer.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "buyer", "status", "payment_status",
            "items", "total", "created_at", "updated_at"
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ["items"]

    def validate_items(self, items):
        if len(items) == 0:
            raise serializers.ValidationError("Order must contain at least 1 item.")
        return items

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(buyer=self.context["request"].user, **validated_data)

        total = Decimal("0.00")

        for item in items_data:
            product = item["product"]

            item_total = item["unit_price"] * Decimal(item["quantity"])
            total += item_total

            OrderItem.objects.create(
                order=order,
                product=product,
                seller=product.seller,
                unit_price=item["unit_price"],
                quantity=item["quantity"],
            )

        order.total = total
        order.save()

        return order
