import requests
import jwt

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
                'redirect_uri': 'http://localhost:5500/google.html'
            })
            data = response.json()
            id_token = data['id_token']
            decoded_user_data = jwt.decode(id_token, options={'verify_signature': False}) # works in PyJWT >= v2.0
            return decoded_user_data
        except:
            return "The token is invalid or expired."