from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_email(user_email, order_id):
    send_mail(
        subject="Your food has been delivered!",
        message=f"Order #{order_id} has just arrived. Enjoy your meal! 🍽️",
        from_email="no-reply@restaurant.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
