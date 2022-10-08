from django.urls import reverse
from django.core import mail
from .setup import AuthenticationTestSetUp


def get_value_from_last_email(
    separator: str, qty: int = 1) -> str | list: 
    '''
    Pull out value(s) from the last message sent by our server,
    generally for pulling out token from link
    '''
    last_message = mail.outbox[0].body
    if not last_message[-1].isalnum():
        last_message = last_message[:-1]

    values: list = last_message.split(separator)[-qty:]
    if qty == 1:
        return values[0]
    return values


class TestRegisterView(AuthenticationTestSetUp):
    def setUp(self) -> None:
        self.url = reverse('auth:register')
        return super().setUp()
    
    def test_register_success(self):
        response = self.client.post(self.url, self.new_user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.new_user_data['email'])
        self.assertEqual(response.data['username'], self.new_user_data['username'])

    def test_register_empty_post_error(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)


class TestVerifyEmailView(AuthenticationTestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.post(self.register_url, self.new_user_data)  # register user
        self.url = reverse('auth:email-verify')

    def test_verify_success(self):
        '''get token from sent email and send it to verify endpoint'''
        # TODO ponyat`
        token = get_value_from_last_email(separator='?token=', qty=1)
        response = self.client.get(self.url, data={'token': token})
        self.assertEqual(response.status_code, 200)


class TestLoginView(AuthenticationTestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('auth:login')

    def test_login_success(self):
        response = self.client.post(self.url, self.user_data)
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['email'], self.user_data['email'])
        self.assertEqual(data['username'], self.user_data['username'])
        self.assertIsNotNone(data['tokens']['access_token'])
        self.assertIsNotNone(data['tokens']['refresh_token'])

    def test_login_unverified_user_error(self):
        self.user.is_verified = False  # make user unverified
        self.user.save()
        response = self.client.post(self.url, self.user_data)
        data = response.data
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['detail'], 'Email is not verified')


class TestPasswordResetViews(AuthenticationTestSetUp):
    def test_password_reset_success(self):
        '''Test all 3 password-reset views'''

        # TEST REQUESTing password reset (RequestPasswordResetView)
        response = self.client.post(reverse('auth:request-password-reset'),
            data={'email': self.user.email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), 
            f'Email with link to reset password was sent to {self.user.email}')

        # TEST TOKEN VALIDATION for password reset (TokenCheckPasswordResetView)
        # prepare url with encoded data as GET query parameters 
        uidb64, token = get_value_from_last_email(separator='/', qty=2)
        url = reverse('auth:confirm-password-reset',
         kwargs={'uidb64': uidb64, 'token': token})         
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('uidb64'), uidb64)
        self.assertEqual(response.data.get('token'), token)

        # TEST PASSWORD RESET via previously received uidb64 and token (PerformPasswordResetSerializer)
        response = self.client.post(reverse('auth:perform-password-reset'),
            data={'new_password': 'newpassword', 'uidb64': uidb64, 'token': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), f'Updated password for {self.user.username}')

        self.assertFalse(self.user.check_password('newpassword'))  # should be False because changes are not applied to DB yet
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))  # should be True after DB refresh
