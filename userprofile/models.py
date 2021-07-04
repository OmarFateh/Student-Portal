from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def user_image(instance, filename):
    """
    Upload the user image into the path and return the uploaded image path.
    """
    return f'Users/{instance.user.full_name}/{filename}'


class BaseTimestamp(models.Model):
    """
    Timestamp abstract model.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class Userprofile(BaseTimestamp):
    """
    Userprofile model.
    """
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # slug = models.CharField(max_length=10, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True)
    # nationality = CountryField()
    phone = models.CharField(max_length=17, null=True)
    address = models.CharField(max_length=256, null=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, null=True)
    photo = models.ImageField(upload_to=user_image, default='user_default.jpg')
    
    class Meta:
        ordering = ['user__full_name']
        
    def __str__ (self):
        # Return user name.
        return self.user.full_name