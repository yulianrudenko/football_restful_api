from core.custom import APIView

from rest_framework import status
from rest_framework.response import Response

from .serializers import ClubSerializer, PlayerSerializer
from .models import Club, Player
from .selectors import (
    get_club,
    get_player
)


class ClubListView(APIView):
    serializer_class = ClubSerializer

    def get(self, request):
        '''List all clubs'''
        clubs_qs = Club.objects.all()
        serializer = self.serializer_class(clubs_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''Create a club'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_club = serializer.save()
        serializer = self.serializer_class(new_club)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


class ClubDetailView(APIView):
    serializer_class = ClubSerializer

    def get(self, request, club_id: int):
        '''Get single club by id'''
        club_qs = get_club(id=club_id)
        serializer = self.serializer_class(club_qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, club_id: int):
        '''Completely update a club by id'''
        club = get_club(id=club_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = serializer.save()
        serializer = self.serializer_class(club)
        return Response(serializer.data, status=status.HTTP_200_OK)    

    def patch(self, request, club_id: int):
        '''Partly update a club by id'''
        club = get_club(id=club_id)
        serializer = self.serializer_class(club, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        club = serializer.save()
        serializer = self.serializer_class(club)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, club_id: int):
        '''Delete a club by id'''
        club = get_club(id=club_id)
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class PlayerListView(APIView):
    serializer_class = PlayerSerializer

    def get(self, request):
        '''List all players'''
        players_qs = Player.objects.all().select_related('club')
        serializer = self.serializer_class(players_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''Create a player'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_player = serializer.save()
        serializer = self.serializer_class(new_player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


class PlayerDetailView(APIView):
    serializer_class = PlayerSerializer

    def get(self, request, player_id: int):
        '''Get single player by id'''
        player_qs = Player.objects.get(id=player_id)
        serializer = self.serializer_class(player_qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, player_id: int):
        '''Completely update a player by id'''
        player = get_player(id=player_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = serializer.save()
        serializer = self.serializer_class(player)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, player_id: int):
        '''Partly update player by id'''
        player = get_player(id=player_id)
        serializer = self.serializer_class(player, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        player = serializer.save()
        serializer = self.serializer_class(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, player_id: int):
        '''Delete a player by id'''
        player = get_player(id=player_id)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
