from core.custom import APIView, paginate_by_page_number
from core import validators

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator


from .serializers import ClubSerializer, PlayerSerializer
from .models import Club, Player
from .services import (
    create_club,    
    update_club, 
    create_player,
    update_player,
)
from .selectors import (
    get_club,
    get_player
)


class ClubListView(APIView):
    class ClubCreateSerializer(serializers.Serializer):
        title = serializers.CharField(
            validators=[validators.name_validator, UniqueValidator(queryset=Club.objects.all())],
            required=True)
        country = serializers.CharField(required=True, validators=[validators.name_validator])

    input_serializer_class = ClubCreateSerializer

    def get(self, request):
        clubs_qs = Club.objects.all()
        page = paginate_by_page_number(qs=clubs_qs, request=request)
        serializer = ClubSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_club = create_club(**serializer.validated_data)
        serializer = ClubSerializer(new_club)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


class ClubDetailView(APIView):
    class ClubUpdateSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, validators=[validators.name_validator])
        country = serializers.CharField(required=False, validators=[validators.name_validator])

    input_serializer_class = ClubUpdateSerializer

    def get(self, request, club_id: int):
        club_qs = get_club(id=club_id)
        serializer = ClubSerializer(club_qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, club_id: int):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_club = update_club(club_id=club_id, **serializer.validated_data)
        serializer = ClubSerializer(updated_club)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    def delete(self, request, club_id: int):
        club = get_club(id=club_id)
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class PlayerListView(APIView):
    class PlayerCreateSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=True, validators=[validators.name_validator])
        last_name = serializers.CharField(required=True, validators=[validators.name_validator])
        age = serializers.IntegerField(required=True)
        club_id = serializers.IntegerField(required=True)

    input_serializer_class = PlayerCreateSerializer

    def get(self, request):
        players_qs = Player.objects.all().select_related('club')
        page = paginate_by_page_number(qs=players_qs, request=request)
        serializer = PlayerSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_player = create_player(**serializer.validated_data)
        serializer = PlayerSerializer(new_player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


class PlayerDetailView(APIView):
    class PlayerUpdateSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False, validators=[validators.name_validator])
        last_name = serializers.CharField(required=False, validators=[validators.name_validator])
        age = serializers.IntegerField(required=False)
        club_id = serializers.IntegerField(required=False)

    input_serializer_class = PlayerUpdateSerializer

    def get(self, request, player_id: int):
        player_qs = Player.objects.get(id=player_id)
        serializer = PlayerSerializer(player_qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, player_id: int):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = update_player(player_id=player_id, **serializer.validated_data)
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, player_id: int):
        player = get_player(id=player_id)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
