from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from .models import MenuItem, Order


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=MenuItem.objects.all(), source="items"
    )

    class Meta:
        model = Order
        fields = ("id", "user", "delivery_time", "items", "item_ids", "created_at")
        read_only_fields = ("user", "created_at")

    def validate_delivery_time(self, value):
        if value < timezone.now() + timedelta(minutes=30):
            raise serializers.ValidationError("Delivery time must be at least 30 minutes from now.")
        return value

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(
            **validated_data, user=self.context["request"].user
        )
        order.items.set(items)
        return order
