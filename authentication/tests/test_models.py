from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .setup import AuthenticationTestSetUp

User = get_user_model()


class TestUserModel(AuthenticationTestSetUp):
    def test_clean_method(self):
        self.new_user_data['password'] = '1234'
        with self.assertRaises(ValidationError):
            User.objects.create_user(**self.new_user_data)
