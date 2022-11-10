from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from faker.providers import profile

from ..models import User

# prepare Faker
fake = Faker()
fake.add_provider(profile.Provider)


class AuthenticationTestSetUp(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        # create fake user ready for testing
        self.user_data = self.__fake_user_data()
        self.user = User.objects.create_user(**self.user_data, is_verified=True)

        # prepare data for new user registration
        self.new_user_data = self.__fake_user_data()
        self.register_url = reverse('auth:register')

    def tearDown(self) -> None:
        return super().tearDown()

    def __fake_user_data(self):
        '''Create a sample User'''
        fake_profile = fake.simple_profile()
        user_data = {
            'email': fake_profile['mail'],
            'username': fake_profile['username'],
            'password': fake.password()
        }
        return user_data
    