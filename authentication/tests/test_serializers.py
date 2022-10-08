from .setup import AuthenticationTestSetUp
from .. import serializers


class TestRegisterSerializer(AuthenticationTestSetUp):
    def test_success(self):
        serializer = serializers.RegisterSerializer(data=self.new_user_data)
        self.assertTrue(serializer.is_valid())
        data = serializer.validated_data
        self.assertCountEqual(data, self.user_data)

    def test_email_taken_error(self):
        self.new_user_data['email'] = self.user.email  # change email to taken one
        serializer = serializers.RegisterSerializer(data=self.new_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual('email' in serializer.errors.keys(), True)
    
    def test_username_taken_error(self):
        self.new_user_data['username'] = self.user.username  # change username to taken one
        serializer = serializers.RegisterSerializer(data=self.new_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual('username' in serializer.errors.keys(), True)

    def test_username_invalid_error(self):
        self.new_user_data['username'] = 'inv@lid'  # change username to taken one
        serializer = serializers.RegisterSerializer(data=self.new_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual('username' in serializer.errors.keys(), True) 


class TestLoginSerializer(AuthenticationTestSetUp):
    def test_success(self):
        serializer = serializers.LoginSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())