from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core import validators

from .models import Club, Player
from .selectors import (
    get_club
)


class ClubSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        validators=[validators.name_validator, UniqueValidator(queryset=Club.objects.all())])
    country = serializers.CharField(validators=[validators.name_validator])

    def create(self, validated_data):
        new_club = Club.objects.create(**validated_data)
        return new_club

    def update(self, club, validated_data):
        if self.partial:  # calling from PATCH
            for attr in validated_data:
                setattr(club, attr, validated_data[attr])

        else:  # calling from PUT
            club.title = validated_data.get('title')
            club.country = validated_data.get('country')

        club.save()
        return club


class PlayerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(validators=[validators.name_validator])
    last_name = serializers.CharField(validators=[validators.name_validator])
    club = serializers.CharField(source='club.title', read_only=True)
    club_id = serializers.IntegerField(write_only=True)
    age = serializers.IntegerField()

    def create(self, validated_data):
        club = get_club(id=validated_data.get('club_id'))
        new_player = Player.objects.create(**validated_data, club=club)
        return new_player

    def update(self, player, validated_data):
        if self.partial:  # calling from PATCH
            for attr in validated_data:
                setattr(player, attr, validated_data[attr])

        else:  # calling from PUT
            player.club = get_club(id=validated_data.get('club_id'))
            player.first_name = validated_data.get('first_name')
            player.last_name = validated_data.get('last_name')
            player.age = validated_data.get('age')
        player.save()
        return player
