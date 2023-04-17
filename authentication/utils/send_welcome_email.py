from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, to, template_name, context):
    # Render the email template
    email_template = render_to_string(template_name, context)
    
    # Create an EmailMessage object
    email = EmailMessage(
        subject,  # Subject of the email
        email_template,  # Content of the email (the rendered template)
        settings.DEFAULT_FROM_EMAIL,  # From email address
        [to],  # List of recipient email addresses
    )
    
    # Send the email
    email.send()