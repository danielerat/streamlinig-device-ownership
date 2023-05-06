from django.db.models.signals import post_save
from authentication.models import User, Profile
from django.dispatch import receiver

from authentication.utils.send_email_templates import send_welcome_email
from authentication.utils.send_text_message import send_text_message_welcome
from authentication.tasks import send_welcome_email_to_new_user, send_welcome_text_to_new_user


@receiver(post_save, sender=User)
def create_profile_for_new_account(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(
            user=user
        )

        if user.email != "":
            try:
                send_welcome_email_to_new_user.delay(
                    user.email, user.get_full_name())
            except:
                print("Error Sending the emial")
        if user.phone_number != "":
            try:
                send_welcome_text_to_new_user.delay(
                    user.phone_number, user.get_full_name())
            except:
                print("Error Sending the Text Message")
