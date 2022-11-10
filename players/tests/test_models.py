from rest_framework.test import APITestCase
from .test_views import PlayerTestSetUp 
from ..models import Club, Player


class ClubModel(APITestCase):
    def test_save_method(self):
        club = Club(title='title', country='  country ')
        club.save()
        self.assertEqual(club.title, 'Title')
        self.assertEqual(club.country, 'Country')


class PlayerModel(PlayerTestSetUp):
    def test_save_method(self):
        player = Player(first_name='fname', last_name='lname',
            age=30, club=self.club)
        player.save()
        self.assertEqual(player.first_name, 'Fname')
        self.assertEqual(player.last_name, 'Lname')