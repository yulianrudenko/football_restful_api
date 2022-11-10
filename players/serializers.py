from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core import validators

from .models import Club, Player


class ClubSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        validators=[validators.name_validator, UniqueValidator(queryset=Club.objects.all())])
    country = serializers.CharField(validators=[validators.name_validator])

    def create(self, validated_data):
        return Club.objects.create(**validated_data)

    def update(self, club, validated_data):
        if self.partial:    # calling from PATCH method
            for attr in validated_data:
                setattr(club, attr, validated_data[attr])

        else:               # calling from PUT method
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
        new_player = Player.objects.create(**validated_data)
        return new_player

    def update(self, player, validated_data):
        if self.partial:  # calling from PATCH method
            for attr in validated_data:
                setattr(player, attr, validated_data[attr])

        else:  # calling from PUT method
            player.club_id = validated_data.get('club_id')
            player.first_name = validated_data.get('first_name')
            player.last_name = validated_data.get('last_name')
            player.age = validated_data.get('age')

        player.save()
        return player
