from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError


def create_user(validated_data):
    try:
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    except DjangoValidationError as e:
        raise ValidationError({'error': e.messages})
    except Exception as e:
        from . import exceptions
        raise exceptions.FailedToCreateUser('Failed to create user.') from e
