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
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    name = models.CharField(verbose_name="Device Name", max_length=255)
    model = models.CharField(verbose_name="Model", max_length=255)
    serial_number = models.CharField(verbose_name="Serial Number", max_length=255, unique=True)
    mac_address = models.CharField(verbose_name="Mac Address", max_length=100, unique=True)
    imei = models.CharField(verbose_name="IMEI Address", max_length=100, unique=True)
    price = models.DecimalField(max_digits=9,decimal_places=2,validators=[MinValueValidator(1)])
    category = models.CharField(choices=DEVICE_CATEGORY_CHOICES,blank=False, default="phone", max_length=50)
    desc = models.TextField(verbose_name="Device Description")
    quality = models.PositiveIntegerField(choices=DEVICE_QUALITY_CHOICES,blank=False,null=False, default=2, validators=[MaxValueValidator(5),MinValueValidator(1)])
    status = models.CharField(choices=DEVICE_AVAILABILITY_CHOICES, null=False,blank=False, default="active", max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Device "+ self.model


class DeviceFirstAssignment(models.Model):
    device=models.OneToOneField(Device,on_delete=models.CASCADE)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="+")
    first_owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# Device images
class DeviceImage(models.Model):
    device=models.ForeignKey(Device, related_name="images",on_delete=models.CASCADE)
    image=models.ImageField(upload_to='device/images/',validators=[validate_file_size])
    def __str__(self):
        return "Image " + self.id


# Warranty of every single device
class Warranty(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, null=True)
    days = models.PositiveSmallIntegerField(
        verbose_name="Warranty Life",
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1100)],
        help_text="Warranty in days",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Warranty {}".format(self.device)


# Device Transfer between Users
class Transfer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    device = models.ForeignKey(Device, on_delete=models.CASCADE,null=False, blank=False)
    transferor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="transferors")
    transferee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="transferees")
    transfer_status = models.CharField(choices=TRANSFER_STATUS,max_length=1, default="P", null=False,blank=False)
    last_confirm = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Transfer #%s" % self.id



# Devices that are published and can be seen by the public for purchase
class Publish(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    isPublished = models.BooleanField(default=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Published %s" % self.device.name
