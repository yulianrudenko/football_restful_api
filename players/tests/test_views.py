from django.urls import reverse
from .setup import PlayerTestSetUp
from ..models import Club, Player


class TestClubListView(PlayerTestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('api:club-list')
    
    def test_list_clubs_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)    
        data = response.json()[0]
        data.pop('id')
        self.assertEqual(data, self.club_data)    

    def test_create_club_success(self):
        response = self.client.post(self.url, self.new_club_data, **self.headers)
        self.assertEqual(response.status_code, 201) 
        data = response.json()
        data.pop('id')
        self.assertEqual(response.json(), self.new_club_data)

    
class TestClubDetailView(PlayerTestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('api:club-detail', args=[self.club.id])

    def test_get_club_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        data.pop('id')
        self.assertEqual(data, self.club_data)

    def test_put_update_club_success(self):
        '''Completely update existing club with new data'''
        response = self.client.put(self.url, self.new_club_data, **self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        data.pop('id')
        self.assertEqual(data, self.new_club_data)

    def test_put_update_club_error(self):
        response = self.client.put(self.url,    # 1
            data={'title': self.new_club_data['title']}, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'country': ['This field is required.']})

        response = self.client.put(self.url,    # 2
            data={'country': self.new_club_data['country']}, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'title': ['This field is required.']})

    def test_patch_update_club_success(self):
        '''Partially update existing club with new data'''
        response = self.client.patch(self.url, 
            data={'title': self.new_club_data['title']}, **self.headers)
        self.assertEqual(response.status_code, 200)
        updated_title = response.json().get('title')
        self.assertNotEqual(updated_title, self.club_data['title'])
        self.assertEqual(updated_title, self.new_club_data['title'])

    def test_delete_club_success(self):
        response = self.client.delete(self.url, **self.headers)
        self.assertEqual(response.status_code, 204)

        # check if club is actually removed from DB 
        with self.assertRaises(Club.DoesNotExist):
            self.club.refresh_from_db()


class TestPlayerListView(PlayerTestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('api:player-list')

    def test_list_players_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)    

    def test_create_player_success(self):
        response = self.client.post(self.url, self.new_player_data, **self.headers)
        self.assertEqual(response.status_code, 201) 
        self.assertTrue('id' in response.json())
        self.assertTrue('club' in response.json())


class TestPlayerDetailView(PlayerTestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('api:player-detail', args=[self.player.id])

    def test_get_player_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('first_name' in response.json())

    def test_put_update_player_success(self):
        '''Completely update existing player with new data'''
        response = self.client.put(self.url, self.new_player_data, **self.headers)
        self.assertEqual(response.status_code, 200)
        resp_first_name = response.json().get('first_name')
        self.assertEqual(resp_first_name, self.new_player_data['first_name'])
        self.assertNotEqual(resp_first_name, self.player.first_name)

    def test_put_update_player_error(self):
        self.new_player_data.pop('club_id')
        response = self.client.put(self.url,    # 1
            data=self.new_player_data, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'club_id': ['This field is required.']})

    def test_patch_update_player_success(self):
        '''Partially update existing player with new data'''
        response = self.client.patch(self.url, 
            data={'first_name': self.new_player_data['first_name']}, **self.headers)
        self.assertEqual(response.status_code, 200)
        updated_first_name = response.json().get('first_name')
        self.assertNotEqual(updated_first_name, self.player_data['first_name'])
        self.assertEqual(updated_first_name, self.new_player_data['first_name'])

    def test_delete_player_success(self):
        response = self.client.delete(self.url, **self.headers)
        self.assertEqual(response.status_code, 204)

        # check if player is actually removed from DB 
        with self.assertRaises(Player.DoesNotExist):
            self.player.refresh_from_db()
