import threading
from django.db.models.signals import post_save
from stream.models import Device, DeviceFirstAssignment
from django.dispatch import receiver
from django.utils import timezone

# When A new Device is added in the system
# -Record who added it (what business owner)
# -To whom they assigned the device to
# -When precisely it was achieved


@receiver(post_save, sender=Device)
def create_device_first_assignment(sender, instance, created, **kwargs):
    if created:
        request = getattr(threading.currentThread(), 'request', None)
        if request and hasattr(request, 'user'):
            holder = request.user
        else:
            holder = instance.owner
        DeviceFirstAssignment.objects.create(
            device=instance,
            holder=holder,
            first_owner=instance.owner
        )
