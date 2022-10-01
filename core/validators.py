from rest_framework.serializers import ValidationError


def name_validator(name: str):
    if not name.isalpha():
        raise ValidationError('Only letters are allowed.')
    return name


def username_validator(name: str):
    if len(name) < 5:
        raise ValidationError('Username must be at least 5 characters length.')
    if not name.isalnum():
        raise ValidationError('Only letters and numbers are allowed.')
    return name