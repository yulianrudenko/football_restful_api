from django.core.mail import EmailMessage
from django.conf import settings

def send_activation_email(subject, body, to):
    email = EmailMessage(subject, body, from_email=settings.EMAIL_FROM_USER, to=[to])
    email.send()
