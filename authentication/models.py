from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
from django.contrib.auth.models import AbstractUser

from authentication.user_manager import CustomUserManager

CHOICES_ACCOUNT_TYPE = (
    ("p", "Personal"),
    ("b", "Business"),
)

# Custom User Model that is Only Unique to this project.


class User(AbstractUser):
    # remove the username field
    username = None

    # add the phone_number field as the new unique identifier
    phone_number = models.CharField(max_length=10, unique=True)

    # add the email and national_id fields
    email = models.EmailField(unique=True)

    # Accound type for users
    account_type = models.CharField(
        choices=CHOICES_ACCOUNT_TYPE, default="p", max_length=2, null=True
    )

    national_id = models.CharField(max_length=16, validators=[
        RegexValidator(
            r'^[0-9]{16}$', 'Only 16-digit numeric values are allowed.')
    ])

    # set the phone_number field as the USERNAME_FIELD
    USERNAME_FIELD = 'phone_number'

    # make the email and national_id fields required
    REQUIRED_FIELDS = ['email', 'national_id']
    # set the CustomUserManager as the default manager
    objects = CustomUserManager()


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default="default.jpg",
                              upload_to=f"profiles/{user.name}")
# Creating the Address Model


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    province = models.CharField(max_length=250, null=True)
    district = models.CharField(max_length=250, null=True)
    sector = models.CharField(max_length=250, null=True)
    street_name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return "{}@{}".format(self.sector, self.street_name)


class BusinessInfo(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.TextField(
        verbose_name="About Business", max_length=250, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return "Business {}".format(self.name)