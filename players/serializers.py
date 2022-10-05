from rest_framework import serializers

from .models import Club, Player


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'title', 'country']


class PlayerSerializer(serializers.ModelSerializer):
    club = serializers.CharField(source='club.title')

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'club', 'age']
