import jwt

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import RegisterSerializer
from .services import create_user


class RegisterView(APIView):
    def post(self, request):
        # validate data and create new user instance
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user_data = serializer.data
        new_user = create_user(**new_user_data)
        # TODO return user inside userserializer
        return Response(new_user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            # TODO: move to services.py
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms='HS256')  # payload == данные или сообщения, передаваемые по сети 
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST) 
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST) 
