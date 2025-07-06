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
        fields = ("id", "user", "delivery_time", "items",
                  "item_ids", "created_at")
        read_only_fields = ("user", "created_at")

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(**validated_data,
                                     user=self.context["request"].user)
        order.items.set(items)
        return order
