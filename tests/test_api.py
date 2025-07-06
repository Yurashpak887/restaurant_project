import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from core.models import MenuItem, Order, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


def authenticate_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client


@pytest.mark.django_db
def test_menu_item_list():
    MenuItem.objects.create(name="Pizza", description="Cheesy", price=10.99)
    MenuItem.objects.create(name="Burger", description="Beefy", price=8.50)

    client = APIClient()
    response = client.get(reverse("menuitem-list"))

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Pizza"


@pytest.mark.django_db
def test_create_order_valid():
    user = CustomUser.objects.create_user(username="tester", password="123")
    item1 = MenuItem.objects.create(name="Sushi", description="Salmon", price=12.50)
    item2 = MenuItem.objects.create(name="Tempura", description="Shrimp", price=9.00)

    client = authenticate_client(user)

    delivery_time = (timezone.now() + timedelta(minutes=45)).isoformat()
    response = client.post(
        reverse("order-list"),
        {
            "delivery_time": delivery_time,
            "item_ids": [item1.id, item2.id]
        },
        format="json"
    )

    assert response.status_code == 201
    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order.items.count() == 2


@pytest.mark.django_db
def test_create_order_too_soon():
    user = CustomUser.objects.create_user(username="tester2", password="123")
    item = MenuItem.objects.create(name="Taco", description="Spicy", price=5.00)

    client = authenticate_client(user)

    delivery_time = (timezone.now() + timedelta(minutes=10)).isoformat()
    response = client.post(
        reverse("order-list"),
        {
            "delivery_time": delivery_time,
            "item_ids": [item.id]
        },
        format="json"
    )

    assert response.status_code == 400
    assert "Delivery time must be at least 30 minutes from now." in str(response.data)


@pytest.mark.django_db
def test_order_list_authenticated():
    user = CustomUser.objects.create_user(username="authuser", password="123")
    item = MenuItem.objects.create(name="Soup", description="Hot", price=4.99)
    order = Order.objects.create(user=user, delivery_time=timezone.now() + timedelta(minutes=40))
    order.items.set([item])

    client = authenticate_client(user)

    response = client.get(reverse("order-list"))

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == order.id


@pytest.mark.django_db
def test_order_list_unauthenticated():
    client = APIClient()
    response = client.get(reverse("order-list"))

    assert response.status_code == 401
