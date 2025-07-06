from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_order_email


class CustomUser(AbstractUser):
    pass

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    delivery_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        min_time = timezone.now() + timedelta(minutes=30)
        if self.delivery_time < min_time:
            raise ValidationError("Delivery time must be at least 30 minutes from now.")

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

