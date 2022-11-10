import jwt
import requests

from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings


class Google:
    """
    Google class to fetch the user data and return it
    """
    @staticmethod
    def validate(auth_token):
        """
        Fetch Google API for id_token using auth token, then decode it
        """
        try:
            response = requests.post('https://accounts.google.com/o/oauth2/token', data={
                'grant_type': 'authorization_code',
                'code': auth_token,
                'client_id': settings.GOOGLE_APP_CLIENT_ID,
                'client_secret': settings.GOOGLE_APP_CLIENT_SECRET,
                'redirect_uri': 'http://localhost:5500/login.html'
            })
            access_token = response.json().get('access_token')
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?alt=json', headers=headers)
            data = response.json()
            return data
            # token = data['id_token']
            # idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_APP_CLIENT_ID)
            # return idinfo
        except:
            return 'The token is invalid or expired.'