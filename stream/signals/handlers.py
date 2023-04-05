from django.db.models.signals import post_save, pre_save
from stream.models import Device, DeviceFirstAssignment, PendingTransfer, Transfer
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=PendingTransfer)
def change_device_transfer_status(sender, instance, created, **kwargs):
    if not created:
        # User Accepts the device.
        if instance.transfer_status == "A":
            # Update New Device Owner
            device = Device.objects.get(pk=instance.device.pk)
            device.owner = instance.transferee
            device.save()
            # Save the Confirmed Transaction
            Transfer.objects.create(
                device=device,
                transferor=instance.transferor,
                transferee=instance.transferee,
                transfer_status="A",
            )
            # Delete the pending device
            instance.delete()
        if instance.transfer_status == "D":
            instance.delete()
