from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from faker.providers import profile
from random import randint

from authentication.tests.setup import AuthenticationTestSetUp

from ..models import Club, Player

# prepare Faker
fake = Faker()
fake.add_provider(profile.Provider)


class PlayerTestSetUp(AuthenticationTestSetUp):
    def setUp(self) -> None:
        super().setUp()

        # create fake club ready for testing
        self.club_data = self.fake_club_data()
        self.club = Club.objects.create(**self.club_data)

        self.new_club_data = self.fake_club_data()  # data for new club creation

        # create fake player ready for testing
        self.player_data = self.fake_player_data()
        self.player = Player.objects.create(**self.player_data)

        self.new_player_data = self.fake_player_data()  # data for new player creation

        # generate acc.token for future authentication
        response = self.client.post(reverse('auth:login'), self.user_data)
        self.access_token = response.data['tokens']['access_token']
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}


    def tearDown(self) -> None:
        return super().tearDown()

    def fake_club_data(self):
        '''Create a sample Club'''
        self.fake_profile = fake.simple_profile()
        fake_club_data = {
            'title': fake.word().title(),
            'country': fake.country().split(' ')[0].capitalize(),
        }
        return fake_club_data

    def fake_player_data(self):
        '''Create a sample Player'''
        player_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'age': randint(18, 44),
            'club_id': self.club.id
        }
        return player_data
    