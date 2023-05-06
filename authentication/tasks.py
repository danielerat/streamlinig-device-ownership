from authentication.utils.send_email_templates import send_welcome_email
from authentication.utils.send_text_message import send_text_message_welcome
from streamlining.celery import celery
from celery import shared_task


@shared_task
def send_welcome_email_to_new_user(to, names):
    print(f"sending welcome message")
    send_welcome_email(to, names)


@shared_task
def send_welcome_text_to_new_user(to, names):
    print(f"sending Text message")
    send_text_message_welcome(to, names)
