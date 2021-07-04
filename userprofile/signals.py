from django.dispatch import receiver
from django.db.models.signals import pre_save

from accounts.utils import unique_slug_generator
from .models import Userprofile


@receiver(pre_save, sender=Userprofile)     # receiver(signal, **kwargs) # to register a signal
def create_teacher_slug(sender, instance, *args, **kwargs):
    """
    Create a unique slug for a teacher before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)