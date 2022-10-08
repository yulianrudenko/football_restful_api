from rest_framework.serializers import ValidationError


def name_validator(name: str):
    for word in name.split(' '):
        if not word.isalpha():
            raise ValidationError('Only letters are allowed.')
    return name
