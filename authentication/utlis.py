from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.timezone import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


def send_activation_email(*, to_user: User) -> None:
    '''Send an activation link to new user's email'''
    
    # prepare body with activation link(containing acccess token)
    protocol = 'http' if settings.DEBUG else 'https'
    domain = settings.SITE_DOMAIN
    email_verify_path = reverse('auth:email_verify')
    access_token = RefreshToken.for_user(to_user).access_token
    access_token.set_exp(lifetime=timedelta(hours=12))
    link = f'{protocol}://{domain}{email_verify_path}?token={str(access_token)}'

    subject='Verify your email'
    body = f'Hi, {to_user.username}! Use link below to verify your email.\n{link}'
    email = EmailMessage(subject, body, from_email=settings.EMAIL_FROM_USER, to=[to_user])
    email.send()
