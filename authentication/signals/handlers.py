from django.db.models.signals import post_save
from authentication.models import User, Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile_for_new_account(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(
            user=user
        )
