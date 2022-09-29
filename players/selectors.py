from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from .models import Club, Player


def get_club(id: int):
    club = Club.objects.filter(id=id)
    if not club:
        raise NotFound(f'No club with id={id} found.')
    return club[0]


def get_player(id: int):
    player = Player.objects.filter(id=id)
    if not player:
        raise NotFound(f'No player with id={id} found.')
    return player[0]
