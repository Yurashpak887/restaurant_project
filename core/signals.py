from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import Order
from .tasks import send_order_email

@receiver(post_save, sender=Order)
def schedule_email_on_order_created(sender, instance, created, **kwargs):
    if created:
        delivery_eta = instance.delivery_time
        send_order_email.apply_async(
            args=[instance.user.email, instance.pk],
            eta=timezone.now() + timedelta(seconds=10)
        )
