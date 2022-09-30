from rest_framework.serializers import ValidationError


def name_validator(name: str):
    if not name.isalpha():
        raise ValidationError('Only letters are allowed.')
    return name
