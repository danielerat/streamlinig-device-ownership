from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def device_transfer_email(to, device):
    # Render the email template
    email_template = render_to_string(
        'emails/device_transfer_confirmation.html', {'device': device})

    # Create an EmailMessage object
    email = EmailMessage(
        "You have a new Device Registered Under your name!",  # Subject of the email
        email_template,  # Content of the email (the rendered template)
        settings.DEFAULT_FROM_EMAIL,  # From email address
        [to],  # List of recipient email addresses
    )
    email.content_subtype = 'html'

    # Send the email
    email.send()
