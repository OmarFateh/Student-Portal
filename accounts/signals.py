from django.dispatch import receiver
from django.db.models.signals import post_save

from userprofile.models import Userprofile
from .models import User


@receiver(post_save, sender=User)     
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create an empty profile once the user is added.
    """
    if created:
        Userprofile.objects.create(user=instance)