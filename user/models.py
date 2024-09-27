from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_realtor(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)

        user.is_realtor = True
        user.save(using=self._db)

        return user 

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)  # Corrected 'fist_name'
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Updated REQUIRED_FIELDS

    def __str__(self):
        return self.email  

class UserProfile(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    address = models.CharField(verbose_name='Address', max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name='Town/City', max_length=100, null=True, blank=True)
    country = models.CharField(verbose_name='Country', max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name='Post Code', max_length=8, null=True, blank=True)
    longitude = models.CharField(verbose_name='Longitude', max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name='Latitude', max_length=50, null=True, blank=True)

    captcha_score = models.FloatField(default=0.0)
    has_profile = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - Profile'