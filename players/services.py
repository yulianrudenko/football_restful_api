from .models import Club, Player
from .selectors import (
    get_club,
    get_player
)

def create_club(**data) -> Club:
    new_club = Club.objects.create(**data)
    return new_club


def update_club(club_id, **data) -> Club:
    club = get_club(id=club_id)
    
    for attr in data:
        setattr(club, attr, data[attr])
    club.save()
    return club


def create_player(**data) -> Player:
    club_id = data.pop('club_id')
    club = get_club(id=club_id)
    new_player = Player.objects.create(**data, club=club)
    return new_player


def update_player(player_id, **data) -> Player:
    player = get_player(id=player_id)
    club_id = data.pop('club_id')
    player.club = get_club(id=club_id)

    for attr in data:
        setattr(player, attr, data[attr])
    player.save()
    return player