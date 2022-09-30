from django.core.exceptions import ValidationError

class PasswordMinimumLengthValidator:
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                "This password must contain at least %(min_length)d characters.",
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return "Your password must contain at least %(min_length)d characters." \
            % {'min_length': self.min_length}