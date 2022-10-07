from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from faker.providers import profile

from ..models import User


class TestSetUp(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        # prepare Faker
        self.fake = Faker()
        self.fake.add_provider(profile.Provider)

        # create fake user ready for testing
        self.user_data = self.fake_user_data()
        self.user = User.objects.create_user(**self.user_data, is_verified=True)

        # prepare data for new user registration
        self.new_user_data = self.fake_user_data()
        self.register_url = reverse('auth:register')

    def tearDown(self) -> None:
        return super().tearDown()

    def fake_user_data(self):
        '''Create a sample User'''
        self.fake_profile = self.fake.simple_profile()
        user_data = {
            'email': self.fake_profile['mail'],
            'username': self.fake_profile['username'],
            'password': self.fake.password()
        }
        return user_data
    