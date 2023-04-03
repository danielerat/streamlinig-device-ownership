from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from uuid import uuid4

from stream.validators import validate_file_size

DEVICE_CATEGORY_CHOICES = (
    ("phone", "Phone"),
    ("computer", "Computer"),
    ("tablet", "Tablet"),
    ("accessory", "Accessory"),
    ("others", "Others"),
)
DEVICE_QUALITY_CHOICES = (
    (1, "One Star"),
    (2, "Two Stars"),
    (3, "Three Stars"),
    (4, "Four Stars"),
    (5, "New"),
)
DEVICE_AVAILABILITY_CHOICES = (
    ("lost", "Lost"),
    ("stolen", "Stolen"),
    ("active", "Active"),
    ("inactive", "Inactive"),
)
TRANSFER_STATUS = (
    ("A", "Approved"),
    ("P", "Pending"),
    ("D", "Denied"),
)
class Device(models.Model):
    id = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid4)
    name = models.CharField(verbose_name="Device Name", max_length=255)
    model = models.CharField(verbose_name="Model", max_length=255)
    serial_number = models.CharField(verbose_name="Serial Number", max_length=255, unique=True)
    mac_address = models.CharField(verbose_name="Mac Address", max_length=100, unique=True)
    imei = models.CharField(verbose_name="IMEI Address", max_length=100, unique=True)
    price = models.DecimalField(max_digits=9,decimal_places=2,validators=[MinValueValidator(1)])
    category = models.CharField(choices=DEVICE_CATEGORY_CHOICES,blank=False, default="phone", max_length=50)
    desc = models.TextField(verbose_name="Device Description")
    quality = models.PositiveIntegerField(choices=DEVICE_QUALITY_CHOICES,blank=False,null=False, default=2, max_length=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    status = models.CharField(choices=DEVICE_AVAILABILITY_CHOICES, null=False,blank=False, default="active", max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Device "+ self.model


class DeviceFirstAssignment(models.Model):
    device=models.OneToOneField(Device,on_delete=models.CASCADE)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
