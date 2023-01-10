from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from ECommerceAuth.models import Customer

user = get_user_model()


@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    print("sender --> ", sender)
    print("Instance --> ", instance)
    print("Created -->", created)
    if created:
        Customer.objects.create(user=instance)
