from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_welcome_email(to, names):
    # Render the email template
    email_template = render_to_string(
        'emails/welcome_email.html', {'names': names})

    # Create an EmailMessage object
    email = EmailMessage(
        'Welcome At Streamlining Device Tracking',  # Subject of the email
        email_template,  # Content of the email (the rendered template)
        settings.DEFAULT_FROM_EMAIL,  # From email address
        [to],  # List of recipient email addresses
    )
    email.content_subtype = 'html'

    # Send the email
    email.send()
