from django.dispatch import receiver
from django.db.models.signals import pre_save

from accounts.utils import unique_slug_generator
from .models import Course


@receiver(pre_save, sender=Course)     # receiver(signal, **kwargs) # to register a signal
def create_course_slug(sender, instance, *args, **kwargs):
    """
    Create a slug for a course before saving.
    """
    instance.slug = unique_slug_generator(instance)