from django.db import models
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Override user model manager.
    """
    def validate_email_address(self, email):
        """
        Take email and check if it's a valid email.
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('You must provide a valid email address.')

    def create_user(self, email, password=None, is_active=False, is_staff=False, is_superuser=False, is_previously_logged_in=False):
        """
        Take email, password, and user's type and create user.
        """
        if email:
            email = self.normalize_email(email)
            self.validate_email_address(email)
        else:    
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.previously_logged_in = is_previously_logged_in
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        """
        Take email and password, and create staffuser.
        """
        user = self.create_user(email, password=password, is_staff=True)    
        return user

    def create_superuser(self, email, password=None):
        """
        Take email and password, and create superuser.
        """
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True, is_active=True)    
        return user


class User(AbstractBaseUser):
    """
    User model.
    """
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False) # can login
    is_staff = models.BooleanField(default=False) # staff user non superuser
    is_superuser = models.BooleanField(default=False) # superuser
    previously_logged_in = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # USERNAME_FIELD and password are required by default.
    
    objects = UserManager()

    def __str__(self):
        return self.email

    def email_user(self, subject, message):
        send_mail(
            subject, # subject  
            message, # message
            'fatehomar0@gmail.com', # from email
            [self.email,], # to email list
            fail_silently=False,
        )
        # email.send()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name 

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True